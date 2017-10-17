# ref: https://github.com/MrLYC/ycyc/tree/master/ycyc/base
def set_default_attr(obj, name, value):
    """
    Set attribute to obj if attribute is not exists
    :param obj: object
    :param name: attribure name
    :param value: attribure value
    :return: if is attribute not exists
    """
    if not hasattr(obj, name):
        setattr(obj, name, value)
        return value
    return getattr(obj, name, value)

def parent_frame():
    """
    Return parent frame of invoker.
    """
    frames = sys._current_frames()
    current_frame = frames[threading.get_ident()]
    invoker_frame = current_frame.f_back
    return invoker_frame and invoker_frame.f_back

class LogFunctionCall(object):
    
    def __init__(self, func=None, args=None, kwargs=None, returned=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.returned = returned

    def __str__(self):
        s_returned = (
            "" if self.returned is None
                    else "-> %s" % str(self.returned)
        )

        args = list(map(str, self.args or ()))
        args.extend(
            "{k}={v}".format(k=str(k), v=str(v))
            for k, v in list(self.kwargs.items()) or ()
        )

        return "{f}({args}){returned}".format(
            f=self.func.__name__ if self.func else "",
            args=", ".join(args),
            returned="" if self.returned is None
                            else "-> %s" % str(self.returned)
        )