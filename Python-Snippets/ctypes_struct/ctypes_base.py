import ctypes
import sys
from imp import reload
from ctypes import *

class IObjStruct:
    @classmethod
    def from_address_(cls, addr):
        t = cls.from_address(addr) # metaclass creates from_address method
        t.value_addr = addr 
        return t


class ObjStruct(ctypes.Structure, IObjStruct):
    _fields_ = [
        # tracing debug
        ("ob_refcnt"    , ctypes.c_ulonglong),
        ("ob_type"      , ctypes.c_void_p)
    ]
    _fields_size_ = 16


class VarObjStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("ob_size"      , ctypes.c_ulonglong)
    ]
    _fields_size_ = ObjStruct._fields_size_ + 8 # 24

