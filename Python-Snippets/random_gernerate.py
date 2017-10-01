# ref: https://www.v2ex.com/t/394944#reply14
import binascii
import random
import hashlib
import os

# binascii.hexlify(os.urandom(10**7)).decode()

# random.choices(string.ascii_letters + string.digits, k=10**7)

# random.choice(string.ascii_letters + string.digits) for _ in range(10**7)

def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    random.seed(
        hashlib.sha256(
            ("%s%s%s" % (
                random.getstate(),
                time.time(),
                'O_O-SECRET_KEY')).encode('utf-8')
        ).digest())
    # return ''.join(random.choice(allowed_chars) for _ in range(length))
    return ''.join(random.choices(allowed_chars, k = length))