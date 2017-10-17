# ref: https://www.zhihu.com/question/29995881
class ExceptionHook :
    	instance = None
	
	def __call__(self, *args, **kwargs) :
		if self.instance is None:
			from IPython.core import ultratb
			self.instance = ultratb.FormattedTB(mode = "Plain", color_scheme = "Linux", call_pdb = 1)
		return self.instance(*args, **kwargs)

