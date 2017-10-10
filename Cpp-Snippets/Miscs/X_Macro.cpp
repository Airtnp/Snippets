//ref: https://www.zhihu.com/question/57089104/answer/151906183


#define STATE_TABLE \
    ENTRY(STATE0, func0) \
    ENTRY(STATE1, func1) \
    ENTRY(STATE2, func2) \
    ... \
    ENTRY(STATEX, funcX) \

#define NUM_STATES N

enum{ 

    #define ENTRY(a,b) a,
    STATE_TABLE
#undef ENTRY
    NUM_STATES
};

p_func_t jumptable[NUM_STATES] = {

#define ENTRY(a,b) b,
    STATE_TABLE
#undef ENTRY

};

#define ENTRY(a,b) static void b(void);

STATE_TABLE

#undef ENTRY

