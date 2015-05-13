# Remove\_extra\_args

	from decorated import remove_extra_args
	
	@remove_extra_args
	def handle(id):
	    pass
	    
	handle(123)
	handle(id=123)
	handle(id=123, timestamp=123456789) # the timestamp argument will be ignored
	
This is convenient when handling GET/POST requests which are usually messed up with additional fields.
