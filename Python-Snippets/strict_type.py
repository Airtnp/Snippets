from typing import TypeVar, Sequence, Tuple

# For any function F: Callable[[Sequence[Any]], Tuple[Any, ...]]
# Generic[T]
# ref: https://www.zhihu.com/question/64385692/answer/219921645
class Strict:
	# Or T = TypeVar('T') + Sequence[T] / Dict[str, T]
	# Or *args: (*(),)
	@staticmethod
	def args(*typeargs : Tuple[...], **typekwargs: dict): 
	        def _1(func):
	            def _2(*args, **kwargs):
	                for arg_idx, (arg, typearg) in enumerate(zip(args, typeargs)):
	                    if not isinstance(arg, typearg):
	                        raise TypeError(f"Type of argnument {arg_idx} should {typearg}")
	                for key in kwargs:
	                    if not isinstance(kwargs[key], typekwargs[key]):
	                        raise TypeError(f"Type of argnument  named {key} should {typekwargs[key]}")
	                return func(*args,**kwargs)
	            return _2
	        return _1

	def ret(*typerets):
	        def _1(func):
	            def _2(*args, **kwargs):
	                ret = func(*args, **kwargs)
	                if len(typerets) > 1:
	                    for ret_idx,(ret_i, typeret) in enumerate(zip(ret, typerets)):
	                        if not isinstance(ret_i, typeret):
	                            raise TypeError(f"Type of return value {ret_idx} should {typeret}")
	                else:
	                    if not isinstance(ret, typerets[0]):
	                        raise TypeError(f"Type of return value should be {typerets[0]}")
	                return ret
	            return _2
	        return _1