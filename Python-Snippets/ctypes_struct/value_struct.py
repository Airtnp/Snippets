from .ctypes_base import *

# c_long : 4 bytes
# c_void_p : 8 bytes
# c_ssize_t : 4 bytes
# c_ulonglong : 8 bytes <- real Py_ssize_t
# use cast new
# reload: reload(sys.modules[ObjStruct.__module__])


class IntStruct(ctypes.Structure, IObjStruct):
    _fields_ = VarObjStruct._fields_ + [
        ("ob_digit"     , ctypes.c_uint32)
    ]    
    _fields_size_ = VarObjStruct._fields_size_ + 8 # 32


    # ob_digit supports only uint32_t
    # no way to convert back to python long
    # don't know why py_object(id(self)) was wrong
    # copy PyLong_AsLong
    def get(self):
        if self.ob_size == -1:
            return -self.ob_digit
        elif self.ob_size == 0:
            return 0
        elif self.ob_size == 1:
            return self.ob_digit
        sz = abs(self.ob_size) - 1
        x = 0
        i = 1 if self.ob_size > 0 else -1
        while sz >= 0:
            x = (x << 30) | c_uint32.from_address(self.value_addr + 24 + sz * 4).value
            sz -= 1
        return x * i


BoolStruct = IntStruct


class BytesStruct(ctypes.Structure, IObjStruct):
    _fields_ = VarObjStruct._fields_ + [
        ("ob_shash", c_longlong),
        ("ob_sval" , c_char)
    ]

    def get(self, endian='little'):
        byte_arr = []
        for i in range(self.ob_size):
            byte_arr.append(int.from_bytes(c_char.from_address(self.value_addr + 32 + i).value, endian))
        return bytes(byte_arr)
        
class DateTimeDeltaStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("hashcode"    , c_longlong),
        ("days"        , c_int),
        ("seconds"     , c_int),
        ("microseconds", c_int)
    ]


class WeakRefStruct(ctypes.Structure, IObjStruct):
    pass

WeakRefStruct._fields_ = ObjStruct._fields_ + [
        ("wr_object"    , c_void_p),
        ("wr_callback"  , c_void_p),
        ("hash"         , c_longlong),
        ("wr_prev"      , POINTER(WeakRefStruct)),
        ("wr_next"      , POINTER(WeakRefStruct))
    ]

