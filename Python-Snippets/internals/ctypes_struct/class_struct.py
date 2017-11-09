from .ctypes_base import *

# A.f
class MethodObject(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("im_func"       , c_void_p), # callable object
        ("im_self"       , c_void_p), # class instance
        ("im_weakreflist", c_void_p)
    ]

# A().f
class InstanceMethodObject(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("func", c_void_p) # function
    ]

