from .ctypes_base import *




class CodeStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("co_argcount"      , c_int),
        ("co_kwonlyargcount", c_int),
        ("co_nlocals"       , c_int),
        ("co_stacksize"     , c_int),
        ("co_flags"         , c_int),
        ("co_firstlineno"   , c_int),
        ("co_code"          , py_object), # opcode bytes
        ("co_consts"        , py_object), # list
        ("co_names"         , py_object), # list of string
        ("co_varnames"      , py_object), # tuple of string
        ("co_freevars"      , py_object), # tuple of string
        ("co_cellvars"      , py_object), # tuple of string
        ("co_cell2arg"      , c_voidp),
        ("co_filename"      , py_object), # unicode
        ("co_name"          , py_object), # unicode
        ("co_lnotab"        , py_object), # string
        ("co_zombieframe"   , c_voidp),
        ("co_weakreflist"   , py_object),
        ("co_extra"         , py_object)
    ]

    def set(self):
        pass
        