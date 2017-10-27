from .ctypes_base import *
from .code_struct import *
from .container_struct import *

PyCFunction = ctypes.CFUNCTYPE(
    py_object,
    py_object,
    py_object
)

class CellStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("ob_ref", c_void_p) # PyObject*
    ]

class MethodDefStruct(ctypes.Structure, IObjStruct):
    _fields_ = [
        ("ml_name" , c_char_p),
        ("ml_meth" , PyCFunction),
        ("ml_flags", c_int),
        ("ml_doc"  , c_char_p)
    ]

class CFunctionStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("m_ml"         , POINTER(MethodDefStruct)),
        ("m_self"       , c_void_p),   # PyObject*
        ("m_module"     , c_void_p),   # PyObject*
        ("m_weakreflist", c_void_p)
    ]

class FunctionStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("func_code"        , POINTER(CodeStruct)),
        ("func_globals"     , POINTER(DictStruct)),
        ("func_defaults"    , POINTER(TupleStruct)),
        ("func_kwdefaults"  , POINTER(DictStruct)),
        ("func_closure"     , POINTER(TupleStruct)), # tuple of cell
        ("func_doc"         , c_void_p),             # PyObject* can be anything
        ("func_name"        , c_void_p),             # string pointer
        ("func_dict"        , POINTER(DictStruct)),
        ("func_weakreflist" , POINTER(ListStruct)),
        ("func_module"      , c_void_p),
        ("func_annotations" , POINTER(DictStruct)),
        ("func_qualname"    , c_void_p)
    ]


class GenStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("gi_frame"         , c_void_p),    # pointer to frame
        ("gi_running"       , c_char),      # True if executed
        ("gi_code"          , POINTER(CodeStruct)),
        ("gi_weakreflist"   , POINTER(ListStruct)),
        ("gi_name"          , c_void_p),    # string
        ("gi_qualname"      , c_void_p)
    ]

class CoroStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("cr_frame"         , c_void_p),    # pointer to frame
        ("cr_running"       , c_char),      # True if executed
        ("cr_code"          , POINTER(CodeStruct)),
        ("cr_weakreflist"   , POINTER(ListStruct)),
        ("cr_name"          , c_void_p),    # string
        ("cr_qualname"      , c_void_p)
    ]

class AsyncGenStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("ag_frame"         , c_void_p),    # pointer to frame
        ("ag_running"       , c_char),      # True if executed
        ("ag_code"          , POINTER(CodeStruct)),
        ("ag_weakreflist"   , POINTER(ListStruct)),
        ("ag_name"          , c_void_p),    # string
        ("ag_qualname"      , c_void_p),
        ("ag_finalizer"     , c_void_p),
        ("ag_hook_inited"   , c_int),
        ("ag_closed"        , c_int)
    ]