# ref: https://github.com/MrLYC/ycyc/blob/master/ycyc/base/contextutils.py
import logging
import six

@contextmanager
def catch(errors=Exception, reraise=None, callback=logger.warning):
    """
    A context manager to catch the exceptions raised from block.
    :param errors: exception or exceptions tuple
    :param reraise: reraise a new exception from catched exception(default: None)
    :param callback: callback when catched a exception(default: logger.warning)
    """
    exec_info = {
        "callback_returned": None,
        "exception": None,
        "ok": True,
    }
    try:
        yield exec_info
    except errors as err:
        exec_info["exception"] = err
        exec_info["ok"] = False
        if callback:
            exec_info["callback_returned"] = callback(err)
        if reraise:
            six.raise_from(reraise, err)


@contextmanager
def subprocessor(*args, **kwg):
    """
    With new subprocess call,terminate it when exit context
    :param args: argument pass to subprocess.Popen
    :param kwg: key word argument pass to subprocess.Popen
    """
    from subprocess import Popen
    processor = Popen(*args, **kwg)
    try:
        yield processor
    finally:
        if processor.poll() is None:
            processor.terminate()
            processor.wait()


@contextmanager
def companion(
    target, auto_start=True, auto_join=True, process=threading.Thread,
):
    """
    Run the target function as block companion.
    :param target: callable object
    :param auto_start: start thread immediately
    :param auto_join: join thread when exit
    """
    processor = process(target=target)
    processor.daemon = True
    if auto_start:
        processor.start()
    try:
        yield processor
    finally:
        if processor.is_alive():
            processor.join()


@contextmanager
def timeout(seconds, interval=None, ticks=None):
    """
    Send KeyboardInterrupt to main thread to terminate it and
    convert it as RuntimeError if timeout.
    :param seconds: timeout seconds
    :param interval: poll interval
    :param ticks: CPU-Bound thread check interval
    """
    import os
    import signal
    import sys

    signal_finished = False
    start = time.time()
    interval = interval or 0.1
    old_ticks = sys.getcheckinterval()

    cur_thread = threading.current_thread()
    assert cur_thread.name == "MainThread"

    def poll_signal():
        now = time.time()
        while not signal_finished and now - start < seconds:
            time.sleep(interval)
            now = time.time()
        if not signal_finished:
            os.kill(os.getpid(), signal.SIGINT)

    with companion(poll_signal, auto_start=False) as poll_thread:
        if seconds > 0:
            poll_thread.start()

        if ticks is not None:
            sys.setcheckinterval(ticks)
        try:
            yield
        except KeyboardInterrupt:
            now = time.time()
            if now - start >= seconds > 0:
                raise RuntimeError("timeout")
            raise
        finally:
            signal_finished = True
            if ticks is not None:
                sys.setcheckinterval(old_ticks)

    
def call_trace(logger=None, name=None):
    """
    Trace a fun call with loger.
    :param loger: logging.Logger
    :param name: function name
    """
    def _(func):
        fname = name or func.__name__

        @functools.wraps(func)
        def f(*args, **kwg):
            fid = id(args) ^ id(kwg)
            logger.info("%s[%d] call", fname, fid)
            try:
                res = func(*args, **kwg)
                logger.info("%s[%s] return", fname, fid)
                return res
            except Exception as err:
                logger.info("%s[%d] got error: %s", fname, fid, err)
                raise
        return f
    return _

class lrucache:
    """
    LRU cache
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if not hasattr(self, "cached_result"):
            result = self.func(instance)
            setattr(instance, self.func.__name__, result)
        return result

def retry(num, errors=Exception):
    """
    Recall func when catched target errors at most num times
    :param num: maximum retry number, 0 for forever.
    :param errors: catch target errors
    """
    if num < 0:
        raise ValueError("num:%d can not less than 0" % num)

    def foo(func):
        @functools.wraps(func)
        def baz(*args, **kwargs):
            i = num and num + 1
            while True:
                try:
                    return func(*args, **kwargs)
                except errors:
                    i -= 1
                    if i == 0:
                        raise
        return baz
    return foo

