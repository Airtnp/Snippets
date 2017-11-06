import ctypes
import sys
from imp import reload
from ctypes import *

value_address = {}  # POINTER(ty) will restricted by __slots__, use global instead
value_offset = {}

class IObjStruct:
    @classmethod
    def from_address_(cls, addr):
        t = cls.from_address(addr) # metaclass creates from_address method
        t.base_value_addr = addr
        t.value_addr = addr
        value_address[id(t)] = addr
        value_offset[id(t)] = 0
        # cls.prepare_addr(cls, t)
        return t

    # Fix LP_Ty from_adddress_ problem
    @staticmethod
    def prepare_addr(cls, ins):
        for i in range(len(cls._fields_)):
            name, ty = cls._fields_[i]
            if name in dir(ins) and ty.__name__.find("LP_") != -1:   # builtin attributes
                not_null = True
                eval_p = "bool(ins.{})"
                if eval(eval_p.format(name)):
                    pass

    @property
    def value_addr(self):
        return value_address[id(self)] + value_offset[id(self)]

    @value_addr.setter
    def value_addr(self, v):
        value_address[id(self)] = v

    def get(self, name):
        item = None
        eval_p = "self.{}".format(name)
        item = eval(eval_p)
        value_address[id(item)] = value_address[id(self)]
        ty = self.__class__
        ity = item.__class__
        if ity.__name__.find("LP_") != -1:
            value_offset[id(item)] = 0
            value_address[id(item)] = c_ulonglong.from_address(value_address[id(self)] + offset).value
        else:
            offset = ty.__dict__[name].offset
            value_offset[id(item)] = value_offset[id(self)] + offset
        return item


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

def KPOINTER(ty):
    oldcls = POINTER(ty)
    old_getitem = oldcls.__getitem__
    def new_getitem(self, offset):
        item = old_getitem(self, offset)
        value_address[id(item)] = value_address[id(self)]
        value_offset[id(item)] = value_offset[id(self)]
        return item
    oldcls.__getitem__ = new_getitem
    return oldcls