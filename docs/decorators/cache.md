# Cache

	from decorated.decorators.cache import SimpleCache
	
	cache = SimpleCache()
	
	@cache.cache('/config/{key}')
	def get_config_from_db(key):
	    print('loading config from db ...')
	    return 'config'
	
	@cache.uncache('/config/{key}')
	def flush_config(key):
	    print('flushing config')
	
	get_config_from_db('config1')
	flush_config('config1')

This will cache the result with the key "/config/{key}" where "{key}" is the actual value of the key parameter.

The code below implements the same function:

	from decorated.decorators.cache import SimpleCache
	
	cache = SimpleCache()
	config_cache = cache.cache('/config/{key}')
	
	@config_cache
	def get_config_from_db(key):
	    print('loading config from db ...')
	    return 'config'
	
	@config_cache.invalidate
	def flush_config(key):
	    print('flushing config')
	
	get_config_from_db('config1')
	flush_config('config1')

If you have pylru installed, you may replace SimpleCache with LruCache.
You may also derive your own class from decorated.decorators.cache.Cache for memcached, redis, etc.
