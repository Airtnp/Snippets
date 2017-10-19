import sys, locale

def detect_encoding():
    expressions = """
        locale.getpreferredencoding()
        type(my_file)
        my_file.encoding
        sys.stdout.isatty()
        sys.stdout.encoding
        sys.stdin.isatty()
        sys.stdin.encoding
        sys.stderr.isatty()
        sys.stderr.encoding
        sys.getdefaultencoding()
        sys.getfilesystemencoding()
    """

    f = open('dummy', 'w')

    for expr in expressions.split():
        value = eval(expr)
        print(expr.rjust(30), '->', repr(value))

def EncodedOutput():
    def __init__(self, enc):
        self.enc = enc
        self.stdout = sys.stdout
        self.stderr = sys.stderr
    def __enter__(self):
        if sys.stdout.encoding is None:
            w = codecs.getwriter(self.enc)
            sys.stdout = w(sys.stdout)
            sys.stderr = w(sys.stderr)
    def __exit__(self, exc_ty, exc_val, tb):
        sys.stdout = self.stdout

import unicodedata
import string

def shave_marks(txt):
    """去掉全部变音符号"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt
        if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)

def shave_marks_latin(txt):
    """把拉丁基字符中所有的变音符号删除"""
    norm_txt = unicodedata.normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue # 忽略拉丁基字符上的变音符号
        keepers.append(c)
        # 如果不是组合字符，那就是新的基字符
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)

