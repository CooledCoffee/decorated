# Timeout

	from decorated import timeout
	
	@timeout(60)
	def download(url):
	    print('Downloading %s ...' % url)
	    
	download('http://test.com/...')
		
A TimeoutError will be raised if download takes more than 60 seconds.

The timeout decorator implements the context manager protocol.
This example below achieve the same functionality.

	from decorated import timeout
	
	def download(url):
	    with timeout(60):
	        print('Downloading %s ...' % url)
	        
	download('http://test.com/...')
	