# ref: http://www.ps.uni-saarland.de/~duchier/python/prolog.py
# Copyright (c) Feb 2000, by Denys Duchier, Universitaet des Saarlandes

"""
This modules implements a rudimentary prolog engine.  Its
purpose is to illustrate the use of continuations to program
a search engine with backtracking and cut.
"""

def bind(var,term,alist):
  """bind var to term in environment alist. return the updated
  environment.  we make a copy so that we don't have to undo on
  backtracking (in essence: we always trail)."""
  alist = alist.copy()
  alist[var]=term
  return alist

def unify(t1,t2,alist,yes,no):
  """attempt to unify t1 with t2 in environment alist.
  yes is the success continuation. no is the failure continuation"""
  t1 = t1.deref(alist)
  t2 = t2.deref(alist)
  if t1 is t2:
    return yes(alist,no)
  elif t1.isVar():
    return yes(bind(t1,t2,alist),no)
  elif t2.isVar():
    return yes(bind(t2,t1,alist),no)
  elif t1.fun!=t2.fun or len(t1.args)!=len(t2.args):
    return no()
  else:
    return unifyN(len(t1.args)-1,t1.args,t2.args,alist,yes,no)

def unifyN(index,list1,list2,alist,yes,no):
  """attempt to unify to sequences of equal lengths"""
  if index<0:
    return yes(alist,no)
  else:
    return unify(list1[index],list2[index],alist,
                 lambda				\
                 alist,no,			\
                 list1=list1,list2=list2,	\
                 index=index-1,yes=yes:		\
                 unifyN(index,list1,list2,alist,yes,no),
                 no)

class Term:
  def deref(self,alist):
    return self
  def isVar(self):
    return 0
  def collectVars(self,list):
    pass
  def instantiate(self,alist,topvars,allvars):
    return self

class Var(Term):
  def __init__(self,name):
    self.name = name
  def deref(self,alist):
    if alist.has_key(self):
      return alist[self].deref(alist)
    else:
      return self
  def isVar(self):
    return 1
  def __str__(self):
    return '?'+str(self.name)
  def collectVars(self,list):
    if not (self in list):
      list.append(self)
  def rename(self,alist):
    if alist.has_key(self):
      return alist[self]
    else:
      v2 = Var(self.name)
      alist[self] = v2
      return v2
  def solve(self,engine,alist,yes,no,entryno):
    t = self.deref(alist)
    if t is self:
      raise "cannot call an uninstantiated literal"
    else:
      return t.solve(engine,alist,yes,no,entryno)
  def instantiate(self,alist,topvars,allvars):
    t = self.deref(alist)
    if t is self:
      if self in topvars:
        return self
      else:
        i = 1
        while 1:
          name = '%s:%d' % (self.name,i)
          if not allvars.has_key(name):
            allvars[name]=1
            var = Var(name)
            alist[self]=var
            topvars.append(var)
            return var
          else:
            i = i+1
    else:
      return t.instantiate(alist,topvars,allvars)

from string import join

class Cons(Term):
  def __init__(self,fun,args):
    self.fun  = fun
    self.args = args
  def __str__(self):
    l = []
    for x in self.args:
      l.append(str(x))
    return str(self.fun)+'('+join(l,',')+')'
  def collectVars(self,list):
    for x in self.args:
      x.collectVars(list)
  def new(self,fun,args):
    return Cons(fun,args)
  def rename(self,alist):
    fun2 = self.fun.rename(alist)
    args2 = []
    for x in self.args:
      args2.append(x.rename(alist))
    return self.new(fun2,args2)
  def solve(self,engine,alist,yes,no,entryno):
    return engine.call(self.fun,self,alist,yes,no,entryno)
  def instantiate(self,alist,topvars,allvars):
    l = []
    for x in self.args:
      l.append(x.instantiate(alist,topvars,allvars))
    return Cons(self.fun,l)

class Atom(Term):
  def __init__(self,name):
    self.fun  = name
    self.args = []
  def __str__(self):
    return str(self.fun)
  def __call__(self,*args):
    return Cons(self,args)
  def rename(self,alist):
    return self
  def solve(self,engine,alist,yes,no,entryno):
    return engine.call(self,self,alist,yes,no,entryno)

class Rule:
  def __init__(self,head,body):
    self.head = head
    self.body = body
  def rename(self,alist=None):
    if alist is None:
      alist = {}
    return Rule(self.head.rename(alist),
                self.body.rename(alist))

AND = Atom('AND')
OR  = Atom('OR')
CUT = Atom('CUT')

class Engine:
  """implements a prolog engine"""
  def __init__(self):
    self.db    = {}
    self.alist = None
    self.no    = None
    self.vars  = None
    self.query = None
  def rule(self,head,*body):
    body = apply(AND,body)
    r = Rule(head,body)
    p = head.fun
    if self.db.has_key(p):
      l = self.db[p]
    else:
      l = []
      self.db[p] = l
    l.append(r)
  def run(self,Q):
    """run a query Q"""
    self.query = Q
    self.alist = None
    self.no    = None
    self.vars  = []
    Q.collectVars(self.vars)
    yes = lambda alist,no,self=self: self.succeed(alist,no)
    no  = lambda self=self : self.fail()
    Q.solve(self,{},yes,no,no)
  def succeed(self,alist,no):
    """this is called when a solution is found"""
    self.alist = alist
    self.no    = no
    print 'yes'
    # all the disgusting stuff below is just so that we can
    # print a coherent and informative answer to the query
    topvars = self.vars[:]
    allvars = {}
    for x in topvars:
      allvars[x.name]=1
    t1 = Cons(None,topvars)
    t2 = Cons(None,(self.query,))
    t3 = Cons(None,(t1,t2))
    t3 = t3.instantiate(alist,topvars,allvars)
    t1,t2 = t3.args
    print str(t2.args[0])
    for i in range(len(self.vars)):
      print '\t'+str(self.vars[i])+' = '+str(t1.args[i])
  def fail(self):
    """this is called when no (more) solution is found"""
    self.alist = None
    self.no    = None
    print 'no'
  def next(self):
    """invoke this to search for the next solution"""
    if self.no:
      self.no()
    else:
      print 'No more'
  def call(self,pred,literal,alist,yes,no,entryno):
    """the main functor of the formula is pred.  We treat specially
    functors for AND, OR and CUT.  For all others, we look in the
    engine's database to find appropriate clauses."""
    if   pred is AND:
      return self.solveAll(0,literal.args,alist,yes,no,entryno)
    elif pred is OR :
      return self.solveSome(0,literal.args,alist,yes,no,entryno)
    elif pred is CUT:
      return yes(alist,entryno)
    else:
      if not self.db.has_key(pred):
        raise "unknown predicate "+str(pred)
      else:
        return self.execute(0,self.db[pred],literal,alist,yes,no,no)
  def solveAll(self,i,l,alist,yes,no,entryno):
    """solve all literals in sequence l"""
    n = len(l)
    if n==0:
      return yes(alist,no)
    elif i==n-1:
      return l[i].solve(self,alist,yes,no,entryno)
    else:
      return l[i].solve(
        self,alist,
        lambda alist,no,i=i+1,l=l,self=self,yes=yes,entryno=entryno:\
        self.solveAll(i,l,alist,yes,no,entryno),
        no,entryno)
  def solveSome(self,i,l,alist,yes,no,entryno):
    """solve one of the literals in sequence l"""
    n = len(l)
    if n==0:
      return no()
    elif i==n-1:
      return l[i].solve(self,alist,yes,no,entryno)
    else:
      return l[i].solve(
        self,alist,yes,
        lambda self=self,i=i+1,l=l,alist=alist,yes=yes,no=no,entryno=entryno: \
        self.solveSome(i,l,alist,yes,no,entryno),
        entryno)
  def execute(self,i,rules,literal,alist,yes,no,entryno):
    """try to solve literal using rules"""
    n = len(rules)
    if i==n-1:
      return self.tryrule(rules[i],literal,alist,yes,no,entryno)
    else:
      return self.tryrule(
        rules[i],literal,alist,yes,
        lambda i=i+1,rules=rules,literal=literal,alist=alist, \
        yes=yes,no=no,entryno=entryno,self=self: \
        self.execute(i,rules,literal,alist,yes,no,entryno),
        entryno)
  def tryrule(self,rule,literal,alist,yes,no,entryno):
    """try to solve literal using rule."""
    # we first rename all variables in the rule so that we can
    # safely use them without risk of clashing with variables
    # already in use.  then we try to unify the literal with
    # the rule's head and if that succeeds we proceed to solve
    # the body of the rule.
    rule = rule.rename()
    return unify(rule.head,literal,alist,
                 lambda alist,no,rule=rule,self=self,yes=yes,entryno=entryno : \
                 rule.body.solve(self,alist,yes,no,entryno),
                 no)

X	= Var('X')
Y	= Var('Y')
Z	= Var('Z')
L	= Var('L')
L1	= Var('L1')
L2	= Var('L2')
L3	= Var('L3')
MEMBER	= Atom('member')
NIL	= Atom('nil')
CONS	= Atom('cons')
APPEND	= Atom('append')
PERMUTE	= Atom('permute')
INSERT	= Atom('insert')
a	= Atom('a')
b	= Atom('b')
c	= Atom('c')
MEMBER1	= Atom('member1')

E = Engine()
E.rule(MEMBER(X,CONS(X,L)))
E.rule(MEMBER(X,CONS(Y,L)),MEMBER(X,L))
E.rule(APPEND(NIL,L,L))
E.rule(APPEND(CONS(X,L1),L2,CONS(X,L3)),APPEND(L1,L2,L3))
E.rule(PERMUTE(NIL,NIL))
E.rule(PERMUTE(CONS(X,L1),L3),AND(PERMUTE(L1,L2),INSERT(X,L2,L3)))
E.rule(INSERT(X,L,CONS(X,L)))
E.rule(INSERT(X,CONS(Y,L1),CONS(Y,L2)),INSERT(X,L1,L2))
E.rule(MEMBER1(X,CONS(X,L)),CUT)
E.rule(MEMBER1(X,CONS(Y,L)),MEMBER1(X,L))