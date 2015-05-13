# Basic

The workflow of the @cache decorator can be decomposed into three phases:

0. init:
A new instance of the cache class is instantiated.
The \_init method is called along with the init arguments.
You can omit this method if your decorator does not have parameter.

0. decorate:
The \_decorate method is called along with the target function.
The return value is used as the decorator.
Normally, you get this return value by calling Function.\_decorate method.

0. call:
Whenever the decorated function is called,
the execution is proxied to the \_call method with the actual arguments.

## Example 1: Decorator without argument

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
	
	@cache
	def get_config_from_db():
	    print('loading config from db ...')
	    return 'config'
	
	print(get_config_from_db()) # will load from db
	print(get_config_from_db()) # will load from cache

## Example 2: Decorator with arguments

	from decorated import Function
	
	class cache(Function):
	    _items = {}
	
	    def _init(self, key=None):
	        self._key = key
	
	    def _decorate(self, func):
	        self._key = func.__name__
	        return super(cache, self)._decorate(func)
	
	    def _call(self, *args, **kw):
	        result = self._items.get(self._key)
	        if result is None:
	            result = super(cache, self)._call(*args, **kw)
	            self._items[self._key] = result
	        return result
	    
	@cache('config')
	def get_config_from_db():
	    print('loading config from db ...')
	    return 'config'
	
	print(get_config_from_db()) # will load from db
	print(get_config_from_db()) # will load from cache

## Example 3: Decorator that can be used with or without arguments

	from decorated import Function
	
	class cache(Function):
	    _items = {}
	    
	    def _init(self, key=None):
	        self._key = key
	        
	    def _decorate(self, func):
	        self._key = func.__name__
	        return super(cache, self)._decorate(func)
	        
	    def _call(self, *args, **kw):
	        result = self._items.get(self._key)
	        if result is None:
	            result = super(cache, self)._call(*args, **kw)
	            self._items[self._key] = result
	        return result
	
	@cache
	def get_config1_from_db():
	    print('loading config1 from db ...')
	    return 'config1'
	
	@cache('config2')
	def get_config2_from_db():
	    print('loading config2 from db ...')
	    return 'config2'
	
	print(get_config1_from_db()) # will load from db
	print(get_config1_from_db()) # will load from cache
	print(get_config2_from_db()) # will load from db
	print(get_config2_from_db()) # will load from cache
