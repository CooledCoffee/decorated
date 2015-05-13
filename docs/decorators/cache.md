# Cache

	from decorated.decorators.cache import SimpleCache
	
	simple_cache = SimpleCache()
	
	@simple_cache.cache('/config/{key}')
	def get_config_from_db(key):
	    print('loading config from db ...')
	    return 'config'
	
	@simple_cache.uncache('/config/{key}')
	def flush_config(key):
	    print('flushing config')
	
	get_config_from_db('config1')
	flush_config('config1')

This will cache the result with the key "/config/{key}" where "{key}" is the actual value of the key parameter.

If you have pylru installed, you may replace SimpleCache with LruCache.
You may also derive your own class from decorated.decorators.cache.Cache for memcached, redis, etc.
