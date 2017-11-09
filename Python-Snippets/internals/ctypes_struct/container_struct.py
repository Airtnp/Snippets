from .ctypes_base import *
from .value_struct import*

class ListStruct(ctypes.Structure, IObjStruct):
    _fields_ = VarObjStruct._fields_ + [
        ("ob_item"      , ctypes.c_void_p),  # PyObject**
        ("allocated"    , ctypes.c_ulonglong)
    ]
    _fields_size_ = VarObjStruct._fields_size_ + 16 # 40


    def get(self, Ty):
        ptr_array = self.ob_size * KPOINTER(Ty)      # KPOINTER(KPOINTER(Ty))
        return ptr_array.from_address(self.ob_item)        


class TupleStruct(ctypes.Structure, IObjStruct):
    _fields_ = VarObjStruct._fields_ + [
        ("ob_item"      , ctypes.c_void_p)  # PyObject* [1]
    ]
    _fields_size_ = VarObjStruct._fields_size_ + 8 # 32
        
    def get(self, Ty):
        ptr_cls = KPOINTER(Ty)
        ptr_array = []
        for i in range(self.ob_size):
            ptr_array.append(ptr_cls.from_address(self.value_addr + 24 + 8 * i))
        return ptr_array
    

class DictKeyIndiceStruct(ctypes.Union):
    _fields_ = [
        ("as_1", c_int8 * 8),
        ("as_2", c_int16 * 4),
        ("as_4", c_int32 * 2),
        ("as_8", c_int64)
    ]

class DictKeyStruct(ctypes.Structure):
    dict_lookup_func = ctypes.CFUNCTYPE(
        c_longlong,
        c_void_p,   # PyDictObject*
        c_void_p,   # PyObject*
        c_longlong, # Py_hash_t
        c_void_p    # PyObject**
    )

    _fields_ = [
        ("dk_refcnt"  , c_longlong),
        ("dk_size"    , c_longlong),
        ("dk_lookup"  , dict_lookup_func),
        ("dk_usable"  , c_longlong),
        ("dk_nentries", c_longlong),
        ("dk_indices" , DictKeyIndiceStruct)
    ]


class DictStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("ma_used"         , c_longlong),
        ("ma_version_tag"  , c_ulonglong),
        ("ma_keys"         , KPOINTER(DictKeyStruct)),
        ("ma_values"       , c_void_p) # PyObject**
    ]

    def get(self, key, Ty):
        pass


class RangeStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("start"    , KPOINTER(IntStruct)),
        ("stop"     , KPOINTER(IntStruct)),
        ("step"     , KPOINTER(IntStruct)),
        ("length"   , KPOINTER(IntStruct))
    ]

    def get(self):
        return [self.start, 
                self.stop,
                self.step,
                self.length]

class SliceStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("start"    , KPOINTER(IntStruct)),
        ("stop"     , KPOINTER(IntStruct)),
        ("step"     , KPOINTER(IntStruct)),
    ]

    def get(self):
        return [self.start, 
                self.stop,
                self.step]


class SetEntryStruct(ctypes.Structure):
    _fields_ = [
        ("key"  , c_void_p),
        ("hash" , c_longlong)
    ]


class SetStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("fill"         , c_longlong),
        ("used"         , c_longlong),
        ("mask"         , c_longlong),
        ("table"        , KPOINTER(SetEntryStruct)),
        ("hash"         , c_longlong),
        ("finger"       , c_longlong),
        ("smalltable"   , SetEntryStruct * 8),
        ("weakreflist"  , KPOINTER(ListStruct))
    ]