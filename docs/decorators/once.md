Once
----

To make sure a function is called only once:

	from decorated import once
	
	@once
	def init():
	    pass
	    
	init() # will call the function
	init() # will be ignored
	
To make sure a function is called only once for a specified value:

	from decorated import once
	
	@once('key')
	def init_config(key):
	    return 'config ' + key
	    
	init_config('a') # will call the function and return 'config a'
	init_config('a') # will not call the function but directly return the previous result 'config a'
	init_config('b') # will call the function and return 'config b'
	
To make sure a function is called only once for a given session:

	from decorated import once, OnceSession
	
	@once
	def check_is_logined(token):
	    if token is None:
	        raise Exception('Not authed.')
	    
	with OnceSession():
	    check_is_logined('token') # will call the function
	    check_is_logined('token') # will be ignored
	with OnceSession():
	    check_is_logined('token') # will call the function because it is in a different session
