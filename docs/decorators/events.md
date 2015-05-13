# Events

	from decorated import event
	
	upload_event = event(('filename', 'data'))
	
	@upload_event
	def upload(filename, data):
	    print('saving ...')
	    
	@upload_event.before
	def before_upload(data):
	    print('received %d bytes' % len(data))
	    
	@upload_event.after
	def after_upload(filename):
	    print('saved as %s' % filename)
	    
	upload('aaa.txt', '!@#$%^&*()')

In a large system, the functions are usually defined in different modules and loosely coupled by events.
If functions are located in different modules, make sure you load those modules before calling the upload function.
Alternatively, you can call events.init('your\_package\_name') to do this for you.