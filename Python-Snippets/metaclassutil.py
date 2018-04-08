# ref: http://manjusaka.itscoder.com/2016/11/18/Someone-tell-me-that-you-think-Python-is-simple/
class TraceAttribute(type):
    def __init__(cls, name, bases, dict):
        __getattribute__o = cls.__getattribute__

        def __getattribute__(self, *args, **kwargs):
            print('__getattribute__:', args, kwargs)
            return __getattribute__o(self, *args, **kwargs)

        cls.__getattribute__ = __getattribute__

class SingleMeta(type):
    def __init__(cls, name, bases, dict):
        cls._instance = None
        __new__o = cls.__new__

        @staticmethod
        def __new__(cls, *args, **kwargs):
            if cls._instance:
                return cls._instance
            cls._instance = cv = __new__o(cls, *args, **kwargs)
            return cv

        cls.__new__ = __new__

