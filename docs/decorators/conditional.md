# Conditional

	from decorated import conditional
	import time
	
	@conditional(condition='seconds != 0')
	def sleep1(seconds):
	    time.sleep(seconds)
	    
	@conditional(condition=lambda seconds: seconds != 0)
	def sleep2(seconds):
	    time.sleep(seconds)
	    
The target function is called only if the condition evaluates to True.
The condition argument can either be a string or a callable.
