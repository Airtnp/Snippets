from .ctypes_base import *

# There are 4 forms of Unicode strings:

"""
- compact ascii:

    * structure = PyASCIIObject
    * test: PyUnicode_IS_COMPACT_ASCII(op)
    * kind = PyUnicode_1BYTE_KIND
    * compact = 1
    * ascii = 1
    * ready = 1
    * (length is the length of the utf8 and wstr strings)
    * (data starts just after the structure)
    * (since ASCII is decoded from UTF-8, the utf8 string are the data)

"""
class ASCIIStateStruct(ctypes.Structure):
    _fields_ = [
        ("interned" , c_uint, 2),
        ("kind"     , c_uint, 3),
        ("compact"  , c_uint, 1),
        ("ascii"    , c_uint, 1),
        ("ready"    , c_uint, 1),
        ("padding"  , c_uint, 24)
    ]


class ASCIIStruct(ctypes.Structure, IObjStruct):
    _fields_ = ObjStruct._fields_ + [
        ("length"   , c_longlong), # number of code points   16 - 23
        ("hash"     , c_longlong), #                         24 - 31
        ("state"    , ASCIIStateStruct),                 #   32 - 36
        ("wstr"     , c_wchar_p)   # null-terminated wchar_t 40 - 48
    ]

class CompactUnicodeStruct(ctypes.Structure, IObjStruct):
    _fields_ = ASCIIStruct._fields_ + [
        ("utf8_length"  , c_longlong), # number of bytes exclusing \0
        ("utf8"         , c_char_p),   # null-terminated UTF-8
        ("wstr_length"  , c_longlong)  # number of code points in wstr
                                       # possible surrogates count as two code points.
    ]

class UnicodeUnionStruct(ctypes.Union):
    _fields_ = [
        ("any"      , c_void_p),
        ("latin1"   , c_uint8),  # Py_UCS1
        ("ucs2"     , c_uint16), # Py_UCS2
        ("ucs4"     , c_uint32)  # Py_UCS4
    ]

class UnicodeStruct(ctypes.Structure, IObjStruct):
    _fields_ = CompactUnicodeStruct._fields_ + [
        ("data", UnicodeUnionStruct), # Canonical, smallest-form Unicode buffer
    ]

    def get(self):
        return self.wstr

# ref: https://stackoverflow.com/questions/35500018/how-to-work-with-utf-16-in-python-ctypes
if sys.version_info[0] > 2:
    unicode = str

def decode_utf16_from_address(address, byteorder='little',
                              c_char=ctypes.c_char):
    if not address:
        return None
    if byteorder not in ('little', 'big'):
        raise ValueError("byteorder must be either 'little' or 'big'")
    chars = []
    while True:
        c1 = c_char.from_address(address).value
        c2 = c_char.from_address(address + 1).value
        if c1 == b'\x00' and c2 == b'\x00':
            break
        chars += [c1, c2]
        address += 2
    if byteorder == 'little':
        return b''.join(chars).decode('utf-16le')
    return b''.join(chars).decode('utf-16be')

class c_utf16le_p(ctypes.c_char_p):
    def __init__(self, value=None):
        super(c_utf16le_p, self).__init__()
        if value is not None:
            self.value = value

    @property
    def value(self,
              c_void_p=ctypes.c_void_p):
        addr = c_void_p.from_buffer(self).value
        return decode_utf16_from_address(addr, 'little')

    @value.setter
    def value(self, value,
              c_char_p=ctypes.c_char_p):
        value = value.encode('utf-16le') + b'\x00'
        c_char_p.value.__set__(self, value)

    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, unicode):
            obj = obj.encode('utf-16le') + b'\x00'
        return super(c_utf16le_p, cls).from_param(obj)

    @classmethod
    def _check_retval_(cls, result):
        return result.value

class UTF16LEField(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls,
                c_void_p=ctypes.c_void_p,
                addressof=ctypes.addressof):
        field_addr = addressof(obj) + getattr(cls, self.name).offset
        addr = c_void_p.from_address(field_addr).value
        return decode_utf16_from_address(addr, 'little')

    def __set__(self, obj, value):
        value = value.encode('utf-16le') + b'\x00'
        setattr(obj, self.name, value)

class Test(ctypes.Structure):
    _fields_ = (('x', ctypes.c_int),
                ('y', ctypes.c_void_p),
                ('_string', ctypes.c_char_p))
    string = UTF16LEField('_string')