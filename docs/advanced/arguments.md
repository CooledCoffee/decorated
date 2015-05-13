# Resolving arguments

It is usually useful to get the arguments of the target function.
This can be easily achieved by the \_resolve_args method.

	from decorated import Function
	
	class cache(Function):
	    _items = {}
	        
	    def _call(self, *args, **kw):
	        args = self._resolve_args(*args, **kw)
	        key = args['key']
	        result = self._items.get(key)
	        if result is None:
	            result = super(cache, self)._call(*args, **kw)
	            self._items[key] = result
	        return result
	
	@cache
	def get_config_from_db(key):
	    print('loading config from db ...')
	    return 'config'
	
	print(get_config_from_db('config1')) # will load from db
	print(get_config_from_db('config1')) # will load from cache
	print(get_config_from_db('config2')) # will load from db
	print(get_config_from_db('config2')) # will load from cache
	