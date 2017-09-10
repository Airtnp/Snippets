import os
import ctypes

FILE_ATTRIBUTE_HIDDEN = 0x02

def write_hidden(file_name, data):
    # For *nix
    prefix = '.' if os.name != 'nt' else ''
    file_name = prefix + file_name

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data)

    if os.name == 'nt':
        FILE_ATTRIBUTE_HIDDEN = 0x02
        kernel32 = ctypes.windll('kernel32', use_last_error=True)
        INVALID_FILE_ATTRIBUTES = -1
        attrs = kernel32.GetFileAttributesW(file_name)
        if attrs == INVALID_FILE_ATTRIBUTES:
            raise ctypes.WinError(ctypes.get_last_error())
        attrs |= FILE_ATTRIBUTE_HIDDEN
        if not kernel32.SetFileAttributesW(file_name, attrs):
            raise ctypes.WinError(ctypes.get_last_error())