# Decorators on class methods

Decorators can be used on class methods. For example,

	from decorated import Function
	
	class cache(Function):
	    _items = {}
	        
	    def _decorate(self, func):
	        self._key = func.__name__
	        return super(cache, self)._decorate(func)
	        
	    def _call(self, *args, **kw):
	        result = self._items.get(self._key)
	        if result is None:
	            result = super(cache, self)._call(*args, **kw)
	            self._items[self._key] = result
	        return result
	
	class Config(object):
	    @cache
	    def get_from_db(self):
	        print('loading config from db ...')
	        return 'config'
	
	config = Config()
	print(config.get_from_db()) # will load from db
	print(config.get_from_db()) # will load from cache
	
The same decorator can also be used on static methods and class methods.
