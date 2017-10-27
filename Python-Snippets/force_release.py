class N():
  def __init__(self):
    self.n = 1

class A():
  def __init__(self):
    self.a = N()
    self.b = self.a
  
  
import sys
import gc
import ctypes
t = A()

print(sys.getrefcount(t.a)) # 3

# or XXStruct.from_address(id(t.a)).ob_refcnt -= 1
ctypes.pythonapi.Py_DecRef(ctypes.py_object(t.a))
ctypes.pythonapi.Py_DecRef(ctypes.py_object(t.a))

# Works for simple object
# ctypes.pythonapi._Py_Dealloc(ctypes.py_object(t.a)) 

# Will collect t.a refcount = 1
gc.collect()