# ref: http://www.ps.uni-saarland.de/~duchier/python/validity.py
# Copyright (c) Feb 2000, by Denys Duchier, Universitaet des Saarlandes

"""
This module implements a validity checker for propositional
formulae.  Its purpose is to illustrate programming with
continuations to implement a `backtracking' search engine.

A formula is represented by an object which responds to
the following methods:

    self.satisfy(alist,yes,no)
    self.falsify(alist,yes,no)

`alist' is a partial assignment of truth values to propositional
variables. `satisfy' attempts to make the formula true, possibly
by appropriately extending the partial assignment. `no' is the
failure continuation.  It takes no argument, and resumes search
in an alternative branch of an earlier choice point. `yes' is the
success continuation and takes 2 arguments: the current partial
assignment alist, and the current failure continuation.

After importing this module, you can test it on various examples
as follows:

IF(AND(OR(P,Q),IF(P,R),IF(Q,R)),R).isValid()

You can also turn on tracing as follows:

Formula.tracing=1
"""

class Formula:
  def isValid(self):
    """a formula is valid iff it cannot be falsified"""
    return self.falsify(
      {},
      lambda alist,no: 0,
      lambda         : 1)
  # satisfy and falsify are wrappers that allow tracing
  # _satisfy and _falsify do the actual work
  tracing = 0
  def satisfy(self,alist,yes,no):
    if Formula.tracing:
      print 'satisfy '+str(self)+' alist='+str(alist)
    return self._satisfy(alist,yes,no)
  def falsify(self,alist,yes,no):
    if Formula.tracing:
      print 'falsify '+str(self)+' alist='+str(alist)
    return self._falsify(alist,yes,no)

class Conjunction(Formula):
  def __init__(self,p,q):
    self.p = p
    self.q = q
  def __str__(self):
    return '('+str(self.p)+' & '+str(self.q)+')'
  def _satisfy(self,alist,yes,no):
    """to satisfy P&Q we must satisfy both P and Q"""
    return self.p.satisfy(
      alist,
      lambda alist,no,self=self,yes=yes: self.q.satisfy(alist,yes,no),
      no)
  def _falsify(self,alist,yes,no):
    """to falsify P&Q we can falsify either P or Q"""
    return self.p.falsify(
      alist, yes,
      lambda self=self,alist=alist,yes=yes,no=no: self.q.falsify(alist,yes,no))

class Disjunction(Formula):
  def __init__(self,p,q):
    self.p = p
    self.q = q
  def __str__(self):
    return '('+str(self.p)+' | '+str(self.q)+')'
  def _satisfy(self,alist,yes,no):
    """to satisfy P|Q we can satisfy either P or Q"""
    return self.p.satisfy(
      alist, yes,
      lambda self=self,alist=alist,yes=yes,no=no: self.q.satisfy(alist,yes,no))
  def _falsify(self,alist,yes,no):
    """to falsify P|Q we must falsify both P and Q"""
    return self.p.falsify(
      alist,
      lambda alist,no,self=self,yes=yes: self.q.falsify(alist,yes,no),
      no)

class Negation(Formula):
  def __init__(self,p):
    self.p = p
  def __str__(self):
    return '!'+str(self.p)
  def _satisfy(self,alist,yes,no):
    """to satisfy !P we must falsify P"""
    return self.p.falsify(alist,yes,no)
  def _falsify(self,alist,yes,no):
    """to falsify !P we must satisfy P"""
    return self.p.satisfy(alist,yes,no)

class Variable(Formula):
  def __init__(self,v):
    self.v = v
  def __str__(self):
    return self.v
  def bind(self,value,alist):
    """returns a new partial assignment that additionally
    assigns the truth `value' to this propositional variable"""
    alist = alist.copy()
    alist[self.v] = value
    return alist
  def assign(self,value,alist,yes,no):
    """attempts to assign the given truth value to this
    proposition variable.  If alist already contains a contradictory
    assignment, the failure continuation is invoked.  Otherwise,
    alist is extended if necessary and the success continuation is
    invoked."""
    if alist.has_key(self.v):
      if alist[self.v]==value:
        return yes(alist,no)
      else:
        return no()
    else:
      return yes(self.bind(value,alist),no)
  def _satisfy(self,alist,yes,no):
    """to satisfy a propositional variable, we must assign it true"""
    return self.assign(1,alist,yes,no)
  def _falsify(self,alist,yes,no):
    """to falsify a propositional variable, we must assign it false"""
    return self.assign(0,alist,yes,no)

def AND(*args):
  """n-ary version of Conjunction"""
  fmla = None
  for x in args:
    if fmla:
      fmla = Conjunction(fmla,x)
    else:
      fmla = x
  return fmla

def OR(*args):
  """n-ary version of Disjunction"""
  fmla = None
  for x in args:
    if fmla:
      fmla = Disjunction(fmla,x)
    else:
      fmla = x
  return fmla

def NOT(x):
  return Negation(x)

def IF(p,q):
  return OR(NOT(p),q)

# For convenience of testing, we create some variables

P = Variable('P')
Q = Variable('Q')
R = Variable('R')

# now we can test it with, e.g.:
# IF(AND(OR(P,Q),IF(P,R),IF(Q,R)),R).isValid()