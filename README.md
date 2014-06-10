Installation
============

pip install decorated

Problems with Traditional Decorators
====================================

Different Forms of Decorators
-----------------------------

Decorators with and without arguments are very different in implementation.

a) without arguments:

	@cache
	def foo():
		pass
		
b) with arguments:

	@cache(key='myfoo')
	def foo():
	    pass

Accessing Arguments
-------------------

You can access the arguments of the wrapped function.
You can also get the parameter names using the inspect module.
However, it is not a minor problem putting these two pieces of information together and figuring out which argument is for which parameter.

Multi-level Decorators
----------------------

You can wrap a function with multi decorators:

	@timeout(seconds=30)
	def foo(a, b=0):
	    pass
	    
	@timeout(seconds=30)
	@cache
	def bar(c, d=0)
	    pass

However, this add even more difficulties to the previous problem.

Solution
========

Decorated solves all the above problems and more.
The core of decorated is a class called "Function" that is similar to the standard python "function".
You can derive your decorators from it.

First Example
-------------

	from decorated import Function
	
	class cache(Function):
	    items = {}
	    
	    def _init(self, key=None):
	        self._key = key
	        
	    def _decorate(self, func):
	        if self._key is None:
	            self._key = func.__name__
	        return super(cache, self)._decorate(func)
	        
	    def _call(self, *args, **kw):
	        d = self._resolve_args(*args, **kw)
	        key = '|'.join([self._key, d['id']])
	        if key in cache.items:
	            return cache.items[key]
	        result = super(cache, self)._call(*args, **kw)
	        cache.items[key] = result
	        return result
	
	# without init argument
	@cache
	def get_user_public_info(id, timestamp=None):
	    return {
	        'id': id,
	        'name': 'Timmy',
	        'timestamp': timestamp,
	    }
	
	# with init argument
	@cache('private_user_info')
	def get_user_private_info(token, id, timestamp=None):
	    return {
	        'id': id,
	        'email': 'timmy@disney.com',
	        'timestamp': timestamp,
	    }
	
	print(get_user_public_info('1'))
	print(get_user_public_info('2', timestamp=12345))
	print(get_user_private_info('11111', '1'))
	print(get_user_private_info('22222', '2', timestamp=12345))

The workflow of Function can be decomposed into three phases:

a) init:
in this phase, a new instance of the cache class is instantiated.
You can deal with init arguments here, but have no access to the target function yet.

b) decorate:
this is where the decoration actually takes place.
In this phase, you gain access to the target function and do some extra init work.
The return value (usually self) is used as the wrapped function.

c) call:
this is executed together with the arguments (\*args & \*\*kw) whenever the function is called.
Usually you will need the \_resolve\_args method to parse the arguments into a dict.

Applying on Class Methods
-------------------------

For normal method:

	class Foo(object):
	    @cache
	    def bar(self):
	        pass

For static method:

	class Foo(object):
	    @staticmethod
	    @cache
	    def bar():
	        pass

For class method:

	class Foo(object):
	    @classmethod
	    @cache
	    def bar(cls):
	        pass

Note that the @staticmethod/@classmethod should always be the outermost.

Context Function
----------------

Context managers are similar with decorators in that they both wrap a block of code.
Sometimes you may need both of them for the same functionality.
For example, you may need timeout both as decorator and as context manager:

	@timeout(60)
	def foo():
		pass
	
	def bar():
	    with timeout(60):
	        pass
	        
In this case, you can derive the timeout from ContextFunction
and override the \_before & \_after methods.
In fact, there is a built-in timeout decorator in the decorated package.
Check out the code for more information.

Built-in Decorators
===================

Decorated comes with some built-in decorators.

cache
-----

	from decorated.decorators.cache import SimpleCache
	
	cache = SimpleCache()
	
	@cache.cache('/{id}/{type}')
	def foo(id, type, name):
	    pass
	    
	@cache.uncache('/{id}/{type}')
	def unfoo(id, type, name):
	    pass
	    
	foo(1, 'type1', 'my name') # will execute the function and store the result in cache with key '/1/type1'
	foo(1, 'type1', 'my name') # will use the result from cache with key '/1/type1'
	foo(2, 'type2', 'your name') # will execute the function because '/2/type2' is missing in cache
	unfoo(1, 'type1', 'my name') # will execute the function and then remove '/1/type1' from cache

If you have pylru installed, you may replace SimpleCache with LruCache.
You may also derive your own class from decorated.decorators.cache.Cache for memcached, redis, etc.

conditional
-----------

	from decorated import conditional
	
	@conditional(condition='amount != 0')
	def save1(id, amount):
	    pass
	    
	@conditional(condition=lambda amount: amount != 0)
	def save2(id, amount):
	    pass
	    
	def _condition(amount):
	    return amount != 0
	@conditional(condition=_condition)
	def save3(id, amount):
	    pass
	    
	class if_non_zero_amount(conditional):
	    def _condition(self, amount):
	        return amount != 0
	@if_non_zero_amount
	def save4(id, amount):
	    pass
	    
All these 4 forms have the same effect. The save function will be called only when amount is not 0.

instantiate
-----------

Suppose @cron is a decorator that calls the target every minute. Instead of writing:

	class Task(object):
	    def run(self)
	        pass
		    
	@cron('* * * * *')
	def run():
	    Task().run()
	    
You can now write:

	from decorated import instantiate
	
	@cron('* * * * *')
	@instantiate(method='run')
	class Task(object):
	    def run(self)
	        pass
	        
The @instantiate decorator creates a wrapper function that instantiates the class and executes the specified method.
The default method is \_\_call\_\_.
Note that you no longer have access to the Task class after this.

once
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
	
	@once('(a, b)')
	def add(a, b, c):
		print(c)
	    return a + b
	    
	add(1, 2, 3) # will call the function
	add(1, 3, 4) # will call the function because the key "(a, b)" if different
	add(1, 2, 4) # will not call the function because the key "(a, b)" if the same as the first call. instead, the previous result will be returned directly
	
To make sure a function is called only once for a given session:

	from decorated import once, OnceSession
	
	@once
	def check_is_logined():
	    pass
	    
	with OnceSession():
	    check_is_logined() # will call the function
	    check_is_logined() # will be ignored
	with OnceSession():
	    check_is_logined() # will call the function because it is called within a different session from the first call
	
This is useful in a web application where you may want a certain function be called only once for a single request.

remove\_extra\_args
-------------------

	from decorated import remove_extra_args
	
	@remove_extra_args
	def handle(id):
	    pass
	    
Now all the following calls are valid:

	handle(123)
	handle(id=123)
	handle(id=123, timestamp=123456789) # the timestamp argument will be removed
	
This is convenient when handling GET/POST requests which are usually messed up with additional fields.

retries
-------

	from decorated import retries
	
	@retries(3, delay=10)
	def download(url):
	    # this function may raise error
	    ...

The retry decorator retries its target (the download function) on error. Maximum retry times is 3 with 10 seconds interval between each retry. If the all 3 times fail, the last error is raised.

synchronized
------------

The effect of @synchronized is similar to its counter-part in java, meaning the functions foo & bar will never be called by two or more threads simultaneously.
You can substitute MemoryLock for FileLock (only works on linux) to synchronize among multi processes.
You can also implement distributed locks using mysql, zookeeper, etc.

	from decorated.decorators.synchronized import MemoryLock
	
	lock = MemoryLock()
	
	@synchronized(lock)
	def foo():
	    pass
	    
	@synchronized(lock)
	def bar():
	    pass
	    
timeout
-------

	from decorated import timeout
	import time
	
	@timeout(60)
	def foo():
		time.sleep(120)
		
A TimeoutError will be raised if foo takes more than 60 seconds.

You can also achieve the same function by:

	from decorated import timeout
	import time
	
	def foo():
	    with timeout(60):
	        time.sleep(120)

events
------

This is a simple yet powerful event mechanism.

	from decorated import Event
	from decorated.util import events
	
	class foo_event(Event):
	    fields = ('id', 'name')
	    ret_field = 'result'
	
	@foo_event
	def foo(id, name, data):
	    print('this is foo')
	    
	@foo_event.before
	def before_foo(id):
	    print('this is called before foo')
	    print('id is %d' % id)
	    
	@foo_event.after
	def after_foo(result):
	    print('this is called after foo')
	    print('the result of foo is %s' % result)
	    
	# this will load all modules under the specified package
	# so that decorator within these modules can actually take effect
	# you can also init with multi packages: events.init(['package1', 'package2'])
	events.init('your_package_name')

In a large system, the event source foo and the event listener before_foo & after_foo are usually defined in different modules to achieve loose coupling.

Combination of Decorators
=========================

You can combine different decorators to achieve more complex functions. For example:

	@once
	@foo_event
	@retries(3)
	def foo(id):
	    pass
	    
	@foo_event.before
	@conditional(condition='id < 0')
	def before_foo():
	    print('bad id, should be non-negative')
	    
Loggingd
========

<a href="https://github.com/CooledCoffee/loggingd" target="_blank">Loggingd</a> is a logging framework based on decorated. You can log using decorators.

	from loggingd import log_enter, log_return, log_error
	
	@log_enter('[DEBUG] Calculating {a} / {b} ...')
	@log_return('Result is {ret}.')
	@log_error('[WARN] Failed to calc.', exc_info=True)
	def divide(a, b):
        return a / b
        
Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
