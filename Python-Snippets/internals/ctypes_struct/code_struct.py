from .ctypes_base import *
from .value_struct import *
from .container_struct import *
from .string_struct import *


class CodeStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("co_argcount"      , c_int),
        ("co_kwonlyargcount", c_int),
        ("co_nlocals"       , c_int),
        ("co_stacksize"     , c_int),
        ("co_flags"         , c_int),
        ("co_firstlineno"   , c_int),
        ("co_code"          , KPOINTER(BytesStruct)), # opcode bytes
        ("co_consts"        , KPOINTER(ListStruct)), # list of string 
        ("co_names"         , KPOINTER(ListStruct)), # list of constants
        ("co_varnames"      , KPOINTER(TupleStruct)), # tuple of string
        ("co_freevars"      , KPOINTER(TupleStruct)), # tuple of string
        ("co_cellvars"      , KPOINTER(TupleStruct)), # tuple of string
        ("co_cell2arg"      , KPOINTER(c_longlong)),
        ("co_filename"      , KPOINTER(UnicodeStruct)), # unicode
        ("co_name"          , KPOINTER(UnicodeStruct)), # unicode
        ("co_lnotab"        , KPOINTER(UnicodeStruct)), # string
        ("co_zombieframe"   , c_void_p),
        ("co_weakreflist"   , py_object),
        ("co_extra"         , c_void_p)
    ]

    def set(self):
        pass
        

class TryBlockStruct(ctypes.Structure):
    _fields_ = [
        ("b_type"   , c_int),
        ("b_handler", c_int),
        ("b_level"  , c_int)
    ]


class FrameStruct(ctypes.Structure, IObjStruct):
    pass 

FrameStruct._fields_ = VarObjStruct._fields_ + [
        ("f_back"           , KPOINTER(FrameStruct)),
        ("f_code"           , KPOINTER(CodeStruct)),
        ("f_builtins"       , KPOINTER(DictStruct)),
        ("f_globals"        , KPOINTER(DictStruct)),
        ("f_valuestack"     , c_void_p), # PyObject**, points after the last local
        ("f_stacktop"       , c_void_p), # PyObject**
        ("f_trace"          , py_object),
        # Generator-only
        ("f_exc_type"       , py_object),
        ("f_exc_value"      , py_object),
        ("f_exc_traceback"  , py_object),
        ("f_gen"            , py_object),
        # Generator-only ends
        ("f_lasti"          , c_int),
        ("f_lineno"         , c_int),
        ("f_iblock"         , c_int),
        ("f_executing"      , c_char),
        ("f_blockstack"     , TryBlockStruct * 20),
        ("f_localsplus"     , c_void_p) # locals + stack, dynamically sized
    ]