#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/delay.h>
#include <linux/spinlock.h>
#include <linux/kthread.h>

/**********************************************************
 Useful macro
**********************************************************/
# define HP_TIMING_NOW(Var) \
 ({ unsigned long long _hi, _lo; \
  asm volatile ("rdtsc" : "=a" (_lo), "=d" (_hi)); \
  (Var) = _hi << 32 | _lo; })

#define __aligned(x)		__attribute__((aligned(x)))
#define WORK_THREAD 		(2)
/**********************************************************
	advanced_lock
**********************************************************/
#define ADV_MAX_NODES	4
struct adv_spinlock {
	struct adv_spinlock *next;
	void *para;
        void (*fn)(void *);
	u16 locked; /* 1 if lock acquired */
	u16 count;  /* nesting count, see qspinlock.c */
	int tail;
};

static DEFINE_PER_CPU_ALIGNED(struct adv_spinlock, adv_nodes[ADV_MAX_NODES]);
#define	_Q_SET_MASK(type)	(((1U << _Q_ ## type ## _BITS) - 1)\
				      << _Q_ ## type ## _OFFSET)
#define _Q_LOCKED_OFFSET	0
#define _Q_LOCKED_BITS		8
#define _Q_LOCKED_MASK		_Q_SET_MASK(LOCKED)

#define _Q_PENDING_OFFSET	(_Q_LOCKED_OFFSET + _Q_LOCKED_BITS)
#if CONFIG_NR_CPUS < (1U << 14)
#define _Q_PENDING_BITS		8
#else
#define _Q_PENDING_BITS		1
#endif
#define _Q_PENDING_MASK		_Q_SET_MASK(PENDING)

#define _Q_TAIL_IDX_OFFSET	(_Q_PENDING_OFFSET + _Q_PENDING_BITS)
#define _Q_TAIL_IDX_BITS	2
#define _Q_TAIL_IDX_MASK	_Q_SET_MASK(TAIL_IDX)

#define _Q_TAIL_CPU_OFFSET	(_Q_TAIL_IDX_OFFSET + _Q_TAIL_IDX_BITS)
#define _Q_TAIL_CPU_BITS	(32 - _Q_TAIL_CPU_OFFSET)
#define _Q_TAIL_CPU_MASK	_Q_SET_MASK(TAIL_CPU)

#define _Q_TAIL_OFFSET		_Q_TAIL_IDX_OFFSET
#define _Q_TAIL_MASK		(_Q_TAIL_IDX_MASK | _Q_TAIL_CPU_MASK)

#define _Q_LOCKED_VAL		(1U << _Q_LOCKED_OFFSET)
#define _Q_PENDING_VAL		(1U << _Q_PENDING_OFFSET)


#define _Q_LOCKED_PENDING_MASK (_Q_LOCKED_MASK | _Q_PENDING_MASK)

struct __qspinlock {
	union {
		atomic_t val;
#ifdef __LITTLE_ENDIAN
		struct {
			u8	locked;
			u8	pending;
		};
		struct {
			u16	locked_pending;
			u16	tail;
		};
#else
		struct {
			u16	tail;
			u16	locked_pending;
		};
		struct {
			u8	reserved[2];
			u8	pending;
			u8	locked;
		};
#endif
	};
};

typedef struct aspinlock {
	atomic_t	val;
} adl_spinlock_t;

/*
 * adv_xchg_tail - Put in the new queue tail code word & retrieve previous one
 * @lock : Pointer to queued spinlock structure
 * @tail : The new queue tail code word
 * Return: The previous queue tail code word
 *
 * xchg(lock, tail)
 *
 * p,*,* -> n,*,* ; prev = xchg(lock, node)
 */
static __always_inline u32 adv_xchg_tail(struct aspinlock *lock, u32 tail)
{
	struct __qspinlock *l = (void *)lock;

	return (u32)xchg(&l->tail, tail >> _Q_TAIL_OFFSET) << _Q_TAIL_OFFSET;
}

static inline u32 adv_encode_tail(int cpu, int idx)
{
	u32 tail;

	tail  = (cpu + 1) << _Q_TAIL_CPU_OFFSET;
	tail |= idx << _Q_TAIL_IDX_OFFSET; /* assume < 4 */

	return tail;
}

static inline struct adv_spinlock *adv_decode_tail(u32 tail)
{
	int cpu = (tail >> _Q_TAIL_CPU_OFFSET) - 1;
	int idx = (tail &  _Q_TAIL_IDX_MASK) >> _Q_TAIL_IDX_OFFSET;

	return per_cpu_ptr(&adv_nodes[idx], cpu);
}

static __always_inline void adv_set_locked(struct aspinlock *lock)
{
	struct __qspinlock *l = (void *)lock;

	WRITE_ONCE(l->locked, _Q_LOCKED_VAL);
}

#ifdef CONFIG_PARAVIRT_SPINLOCKS
#define _a_queued_spin_lock_slowpath	native_queued_spin_lock_slowpath
#endif
#ifndef arch_mcs_spin_lock_contended
/*
 * Using smp_load_acquire() provides a memory barrier that ensures
 * subsequent operations happen after the lock is acquired.
 */
#define arch_adv_spin_lock_contended(l)					\
do {									\
	while (!(smp_load_acquire(l)))					\
		cpu_relax_lowlatency();					\
} while (0)
#endif

#ifndef arch_adv_spin_unlock_contended
/*
 * smp_store_release() provides a memory barrier to ensure all
 * operations in the critical section has been completed before
 * unlocking.
 */
#define arch_adv_spin_unlock_contended(l)				\
	smp_store_release((l), 1)
#endif
static __always_inline int adv_queued_spin_trylock(struct aspinlock *lock)
{
	if (!atomic_read(&lock->val) &&
	   (atomic_cmpxchg(&lock->val, 0, _Q_LOCKED_VAL) == 0))
		return 1;
	return 0;
}


void  adv_queued_spin_lock_slowpath(struct aspinlock *lock, u32 val, void (*fn)(void *), void *para)
{
	struct adv_spinlock *prev, *next, *node;
	u32  old, tail;
	int idx;

	node = this_cpu_ptr(&adv_nodes[0]);
	idx = node->count++;
	tail = adv_encode_tail(smp_processor_id(), idx);

	node += idx;
	node->locked = 0;
	node->next = NULL;
	node->fn = fn;
	node->para = para;
	node->tail = tail;

	if (adv_queued_spin_trylock(lock)) {
		this_cpu_dec(adv_nodes[0].count);
		fn(para);
		atomic_sub(_Q_LOCKED_VAL, &lock->val);
		return;
	}

	old = adv_xchg_tail(lock, tail);

	if (old & _Q_TAIL_MASK) {
		prev = adv_decode_tail(old);
		WRITE_ONCE(prev->next, node);
		arch_adv_spin_lock_contended(&node->locked);
		this_cpu_dec(adv_nodes[0].count);
		return;
	}
	

	while ((val = smp_load_acquire(&lock->val.counter)) & _Q_LOCKED_PENDING_MASK)
		cpu_relax();

	adv_set_locked(lock);

	old = adv_xchg_tail(lock, 0);
repeat:	
	tail = node->tail;
	if(old == tail) {
		goto end;
	}

	while (!(next = READ_ONCE(node->next)))
		cpu_relax();

	node->fn(node->para);
	arch_adv_spin_unlock_contended(&node->locked);

	tail = next->tail;
	if(old != tail) {
		while (!(node = READ_ONCE(next->next)))
			cpu_relax();
		
		next->fn(next->para);				
		arch_adv_spin_unlock_contended(&next->locked);
		goto repeat;
		
	} else
		node = next;

end:
	node->fn(node->para);				
	arch_adv_spin_unlock_contended(&node->locked);

	this_cpu_dec(adv_nodes[0].count);
	atomic_sub(_Q_LOCKED_VAL, &lock->val);
		
}

static void __always_inline adv_spin_lock(struct aspinlock *lock, void (*fn)(void *), void *para)
{
	u32 val;

	val = atomic_cmpxchg(&lock->val, 0, _Q_LOCKED_VAL);
	if (likely(val == 0)) {
		fn(para);
		atomic_sub(_Q_LOCKED_VAL, &lock->val);
		return;
	}
	adv_queued_spin_lock_slowpath(lock, val, fn, para);
}
/**********************************************************
mcs lock
**********************************************************/

#define MAX_NODES	4

struct mcs_spinlock {
	struct mcs_spinlock *next;
	int locked; /* 1 if lock acquired */
	int count;  /* nesting count, see qspinlock.c */
};

static DEFINE_PER_CPU_ALIGNED(struct mcs_spinlock, mcs_nodes[MAX_NODES]);
#if _Q_PENDING_BITS == 8
/**
 * clear_pending_set_locked - take ownership and clear the pending bit.
 * @lock: Pointer to queued spinlock structure
 *
 * *,1,0 -> *,0,1
 *
 * Lock stealing is not allowed if this function is used.
 */
static __always_inline void clear_pending_set_locked(struct qspinlock *lock)
{
	struct __qspinlock *l = (void *)lock;

	WRITE_ONCE(l->locked_pending, _Q_LOCKED_VAL);
}

/*
 * xchg_tail - Put in the new queue tail code word & retrieve previous one
 * @lock : Pointer to queued spinlock structure
 * @tail : The new queue tail code word
 * Return: The previous queue tail code word
 *
 * xchg(lock, tail)
 *
 * p,*,* -> n,*,* ; prev = xchg(lock, node)
 */
static __always_inline u32 xchg_tail(struct qspinlock *lock, u32 tail)
{
	struct __qspinlock *l = (void *)lock;

	return (u32)xchg(&l->tail, tail >> _Q_TAIL_OFFSET) << _Q_TAIL_OFFSET;
}

#else /* _Q_PENDING_BITS == 8 */

/**
 * clear_pending_set_locked - take ownership and clear the pending bit.
 * @lock: Pointer to queued spinlock structure
 *
 * *,1,0 -> *,0,1
 */
static __always_inline void clear_pending_set_locked(struct qspinlock *lock)
{
	atomic_add(-_Q_PENDING_VAL + _Q_LOCKED_VAL, &lock->val);
}

/**
 * xchg_tail - Put in the new queue tail code word & retrieve previous one
 * @lock : Pointer to queued spinlock structure
 * @tail : The new queue tail code word
 * Return: The previous queue tail code word
 *
 * xchg(lock, tail)
 *
 * p,*,* -> n,*,* ; prev = xchg(lock, node)
 */
static __always_inline u32 xchg_tail(struct qspinlock *lock, u32 tail)
{
	u32 old, new, val = atomic_read(&lock->val);

	for (;;) {
		new = (val & _Q_LOCKED_PENDING_MASK) | tail;
		old = atomic_cmpxchg(&lock->val, val, new);
		if (old == val)
			break;

		val = old;
	}
	return old;
}
#endif /* _Q_PENDING_BITS == 8 */


static inline u32 encode_tail(int cpu, int idx)
{
	u32 tail;

	tail  = (cpu + 1) << _Q_TAIL_CPU_OFFSET;
	tail |= idx << _Q_TAIL_IDX_OFFSET; /* assume < 4 */

	return tail;
}

static inline struct mcs_spinlock *decode_tail(u32 tail)
{
	int cpu = (tail >> _Q_TAIL_CPU_OFFSET) - 1;
	int idx = (tail &  _Q_TAIL_IDX_MASK) >> _Q_TAIL_IDX_OFFSET;

	return per_cpu_ptr(&mcs_nodes[idx], cpu);
}

static __always_inline void set_locked(struct qspinlock *lock)
{
	struct __qspinlock *l = (void *)lock;

	WRITE_ONCE(l->locked, _Q_LOCKED_VAL);
}
static __always_inline void __pv_init_node(struct mcs_spinlock *node) { }
static __always_inline void __pv_wait_node(struct mcs_spinlock *node) { }
static __always_inline void __pv_kick_node(struct qspinlock *lock,
					   struct mcs_spinlock *node) { }
static __always_inline void __pv_wait_head(struct qspinlock *lock,
					   struct mcs_spinlock *node) { }


#define pv_enabled()		false

#define pv_init_node		__pv_init_node
#define pv_wait_node		__pv_wait_node
#define pv_kick_node		__pv_kick_node
#define pv_wait_head		__pv_wait_head

#ifdef CONFIG_PARAVIRT_SPINLOCKS
#define org_queued_spin_lock_slowpath	native_queued_spin_lock_slowpath
#endif
#ifndef arch_mcs_spin_lock_contended
/*
 * Using smp_load_acquire() provides a memory barrier that ensures
 * subsequent operations happen after the lock is acquired.
 */
#define arch_mcs_spin_lock_contended(l)					\
do {									\
	while (!(smp_load_acquire(l)))					\
		cpu_relax_lowlatency();					\
} while (0)
#endif

#ifndef arch_mcs_spin_unlock_contended
/*
 * smp_store_release() provides a memory barrier to ensure all
 * operations in the critical section has been completed before
 * unlocking.
 */
#define arch_mcs_spin_unlock_contended(l)				\
	smp_store_release((l), 1)
#endif

	//__raw_cmpxchg((ptr), (old), (new), (size), LOCK_PREFIX)
static __always_inline void _queued_pending_lock(struct qspinlock *lock)
{
	struct __qspinlock *l = (void *)lock;
	while(cmpxchg(&l->locked_pending, _Q_PENDING_VAL, _Q_LOCKED_VAL) != _Q_LOCKED_VAL)
		cpu_relax();
}

void  org_queued_spin_lock_slowpath(struct qspinlock *lock, u32 val)
{
	struct mcs_spinlock *prev, *next, *node;
	u32 new, old, tail;
	int idx;

	BUILD_BUG_ON(CONFIG_NR_CPUS >= (1U << _Q_TAIL_CPU_BITS));

	if (pv_enabled())
		goto queue;

	if (virt_spin_lock(lock))
		return;

	/*
	 * wait for in-progress pending->locked hand-overs
	 *
	 * 0,1,0 -> 0,0,1
	 */
	
	if (val == _Q_PENDING_VAL) {
		while ((val = atomic_read(&lock->val)) == _Q_PENDING_VAL)
			cpu_relax();
	}

	/*
	 * trylock || pending
	 *
	 * 0,0,0 -> 0,0,1 ; trylock
	 * 0,0,1 -> 0,1,1 ; pending
	 */
	for (;;) {
		/*
		 * If we observe any contention; queue.
		 */
		if (val & ~_Q_LOCKED_MASK)
			goto queue;

		new = _Q_LOCKED_VAL;
		if (val == new)
			new |= _Q_PENDING_VAL;

		old = atomic_cmpxchg(&lock->val, val, new);
		if (old == val)
			break;

		val = old;
	}

	/*
	 * we won the trylock
	 */
	if (new == _Q_LOCKED_VAL)
		return;

	/*
	 * we're pending, wait for the owner to go away.
	 *
	 * *,1,1 -> *,1,0
	 *
	 * this wait loop must be a load-acquire such that we match the
	 * store-release that clears the locked bit and create lock
	 * sequentiality; this is because not all clear_pending_set_locked()
	 * implementations imply full barriers.
	 */
	
 	
	while ((val = smp_load_acquire(&lock->val.counter)) & _Q_LOCKED_MASK) {
		cpu_relax();
	}
	/*
	 * take ownership and clear the pending bit.
	 *
	 * *,1,0 -> *,0,1
	 */
	clear_pending_set_locked(lock);
	return;

	/*
	 * End of pending bit optimistic spinning and beginning of MCS
	 * queuing.
	 */
queue:
	node = this_cpu_ptr(&mcs_nodes[0]);
	idx = node->count++;
	tail = encode_tail(smp_processor_id(), idx);

	node += idx;
	node->locked = 0;
	node->next = NULL;
	pv_init_node(node);

	/*
	 * We touched a (possibly) cold cacheline in the per-cpu queue node;
	 * attempt the trylock once more in the hope someone let go while we
	 * weren't watching.
	 */
	if (queued_spin_trylock(lock))
		goto release;

	/*
	 * We have already touched the queueing cacheline; don't bother with
	 * pending stuff.
	 *
	 * p,*,* -> n,*,*
	 */
	old = xchg_tail(lock, tail);

	/*
	 * if there was a previous node; link it and wait until reaching the
	 * head of the waitqueue.
	 */
	if (old & _Q_TAIL_MASK) {
		prev = decode_tail(old);
		WRITE_ONCE(prev->next, node);

		pv_wait_node(node);
		arch_mcs_spin_lock_contended(&node->locked);
	}

	/*
	 * we're at the head of the waitqueue, wait for the owner & pending to
	 * go away.
	 *
	 * *,x,y -> *,0,0
	 *
	 * this wait loop must use a load-acquire such that we match the
	 * store-release that clears the locked bit and create lock
	 * sequentiality; this is because the set_locked() function below
	 * does not imply a full barrier.
	 *
	 */
	pv_wait_head(lock, node);
	while ((val = smp_load_acquire(&lock->val.counter)) & _Q_LOCKED_PENDING_MASK) {
		cpu_relax();
	}

	/*
	 * claim the lock:
	 *
	 * n,0,0 -> 0,0,1 : lock, uncontended
	 * *,0,0 -> *,0,1 : lock, contended
	 *
	 * If the queue head is the only one in the queue (lock value == tail),
	 * clear the tail code and grab the lock. Otherwise, we only need
	 * to grab the lock.
	 */
	for (;;) {
		if (val != tail) {
			set_locked(lock);
			break;
		}
		old = atomic_cmpxchg(&lock->val, val, _Q_LOCKED_VAL);
		if (old == val)
			goto release;	/* No contention */

		val = old;
	}

	/*
	 * contended path; wait for next, release.
	 */
	while (!(next = READ_ONCE(node->next)))
		cpu_relax();

	arch_mcs_spin_unlock_contended(&next->locked);
	pv_kick_node(lock, next);

release:
	/*
	 * release the node
	 */
	this_cpu_dec(mcs_nodes[0].count);
}

static __always_inline void _queued_spin_lock(struct qspinlock *lock)
{
	u32 val;

	val = atomic_cmpxchg(&lock->val, 0, _Q_LOCKED_VAL);
	if (likely(val == 0))
		return;
	org_queued_spin_lock_slowpath(lock, val);
}

static __always_inline void _queued_spin_unlock(struct qspinlock *lock)
{
	/*
	 * smp_mb__before_atomic() in order to guarantee release semantics
	 */
	//smp_mb__before_atomic_dec();
	atomic_sub(_Q_LOCKED_VAL, &lock->val);
}
/********************************ticket spin lock ******************************
 * 
 *
 * ****************************************************************************/
typedef struct arch_spinlock {
	union {
		__ticketpair_t head_tail;
		struct __raw_tickets {
			__ticket_t head, tail;
		} tickets;
	};
} arch_spinlock_ticket;

static inline int  __tickets_equal(__ticket_t one, __ticket_t two)
{
	return !((one ^ two) & ~TICKET_SLOWPATH_FLAG);
}

static inline void __ticket_check_and_clear_slowpath(arch_spinlock_ticket *lock,
							__ticket_t head)
{
	if (head & TICKET_SLOWPATH_FLAG) {
		arch_spinlock_ticket old, new;

		old.tickets.head = head;
		new.tickets.head = head & ~TICKET_SLOWPATH_FLAG;
		old.tickets.tail = new.tickets.head + TICKET_LOCK_INC;
		new.tickets.tail = old.tickets.tail;

		/* try to clear slowpath flag when there are no contenders */
		cmpxchg(&lock->head_tail, old.head_tail, new.head_tail);
	}
}
static __always_inline void ticket_spin_lock(arch_spinlock_ticket *lock)
{
	register struct __raw_tickets inc = { .tail = TICKET_LOCK_INC };

	inc = xadd(&lock->tickets, inc);
	if (likely(inc.head == inc.tail))
		goto out;

	for (;;) {
		unsigned count = SPIN_THRESHOLD;

		do {
			inc.head = READ_ONCE(lock->tickets.head);
			if (__tickets_equal(inc.head, inc.tail))
				goto clear_slowpath;
			cpu_relax();
		} while (--count);
	}
clear_slowpath:
	__ticket_check_and_clear_slowpath(lock, inc.head);
out:
	barrier();	/* make sure nothing creeps before the lock is taken */
}

static __always_inline void ticket_spin_unlock(arch_spinlock_ticket *lock)
{
	if (TICKET_SLOWPATH_FLAG &&
		static_key_false(&paravirt_ticketlocks_enabled)) {
		__ticket_t head;

		BUILD_BUG_ON(((__ticket_t)NR_CPUS) != NR_CPUS);

		head = xadd(&lock->tickets.head, TICKET_LOCK_INC);

		if (unlikely(head & TICKET_SLOWPATH_FLAG)) {
			head &= ~TICKET_SLOWPATH_FLAG;
		}
	} else
		__add(&lock->tickets.head, TICKET_LOCK_INC, UNLOCK_LOCK_PREFIX);
}

static  void atomic_addq(unsigned long i, unsigned long *v)
{
	asm volatile( " lock addq %1,%0"
		     : "+m" (*v)
		     : "ir" (i));
}
static void *work_thread_handle[WORK_THREAD];
static unsigned long _total_ = 0;
/**********************************************************
 Global data
**********************************************************/
static char tmp_data[L1_CACHE_BYTES*4];
static struct qspinlock q_lock __aligned(L1_CACHE_BYTES);
static struct aspinlock a_lock __aligned(L1_CACHE_BYTES);
static arch_spinlock_ticket t_lock __aligned(L1_CACHE_BYTES);
static int  r_lock __aligned(L1_CACHE_BYTES);
static unsigned long  total_number __aligned(L1_CACHE_BYTES);
void spin_work(void *para)
{
	char dummy = (int)(long)para;
	memset(tmp_data, dummy ,sizeof(char) * L1_CACHE_BYTES*1 );
	total_number += 1;
	return ;
}
#define QUEUED_SPINLOCK (0)
#define ADVANCED_SPINLOCK (1)
#define TICKET_SPINLOCK (0)
static int set_bind(int cpu)
{
    cpumask_var_t new_mask;

    if (!zalloc_cpumask_var(&new_mask, GFP_KERNEL))
        return -ENOMEM;
    cpumask_set_cpu(cpu, new_mask);
    set_cpus_allowed_ptr(current, new_mask);
    free_cpumask_var(new_mask);
    return 0;
}


static int work_thread(void *para)
{
	unsigned long i = 20000;
	unsigned long start, end;
	int cpu = (int)(long)para;
	set_bind(cpu);
	HP_TIMING_NOW(start);
	while (i--) {
		
#if QUEUED_SPINLOCK 
		_queued_spin_lock(&q_lock);
#elif TICKET_SPINLOCK	
		ticket_spin_lock(&t_lock);
#elif ADVANCED_SPINLOCK	
		adv_spin_lock(&a_lock, spin_work, para);
#endif

#if !ADVANCED_SPINLOCK	
		 spin_work(para);
#endif

#if QUEUED_SPINLOCK 
		_queued_spin_unlock(&q_lock);
#elif ADVANCED_SPINLOCK	
		;
#elif TICKET_SPINLOCK
		ticket_spin_unlock(&t_lock);
#endif
		
	}
	HP_TIMING_NOW(end);
	atomic_addq(end - start, &_total_);		 
	do {
		schedule();
	}while(!kthread_should_stop());

	return 0;
}

static int __init my_init (void)
{
	int i;

	q_lock.val.counter = 0;
	a_lock.val.counter = 0;
	t_lock.head_tail = 0;
	r_lock = 0;
	total_number = 0;
	for (i = 0; i < WORK_THREAD; i++)
		work_thread_handle[i] = kthread_run(work_thread, (void*)(long)i, "test_thread_%d", i);
	
	return 0;
}

static void __exit my_exit (void)
{
	int i;

	for (i = 0; i < WORK_THREAD; i++)  {
		kthread_stop(work_thread_handle[i]);
	}
	printk("\n all cost time is %ld, total_number is %d\n", _total_, total_number);
}

module_init(my_init);
module_exit(my_exit);

MODULE_LICENSE("GPL");
