# Retries

	from decorated import retries
	
	@retries(3, delay=10)
	def download(url):
	    print('Downloading %s ...' % url)
	    
	download('http://test.com/...')

The retries decorator retries its target function on error.
Maximum call times in the above example is 4 (1 original call + 3 retries) with 10 seconds interval between each retry.
If all the 4 calls fail, the last error is raised.
