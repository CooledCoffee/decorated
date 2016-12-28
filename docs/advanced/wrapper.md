# Wrapper Decorator

Usually, you write a decorator to do something before or after calling the target function.
Such behaviors can be implemented using the WrapperFunction which is a sub-class of the Function class.
For example,

	from decorated import WrapperFunction
	
	class log(WrapperFunction):
	    _items = {}
	        
	    def _before(self, *args, **kw):
	        print('before foo')
	    
	    def _after(self, ret, *args, **kw):
	        print('after foo')
	
	@log
	def foo():
	    print('inside foo')
	
	foo()
