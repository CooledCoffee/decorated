Introduction
============

Decorated aims to ease the uses of decorators. It provides a fundemental class "Function" that is similar to the standard python "function". You can derive your decorator from this Function class.

Different Forms of Decorators
-----------------------------

One major problem with normal decorators is that they come in two forms:

a) without arguments:

	@cache
	def foo():
		pass
		
b) with arguments:

	@cache(expires=86400)
	def foo():
	    pass
	    
Now it is difficult for the cache decorator to handle both situations. Of course you can change the first form to

	@cache()
	def foo():
	    pass
	
But it is not only ugly but also prune to mistake.

Now if you use Function to implement the decorator, it will be something like this:

	class cache(Function):
	    def _init(self, expires=3600):
	        self._expires = expires
	        
	    def _call(self, *args, **kw):
	        # if cached then return directly
	        ...
	    	result = super(cache, self)._call(*args, **kw)
	    	# cache the result
	    	...
	    	return result

The Function class make sure both _init and _call are called in all situations.

Accessing Arguments
-------------------

Another common issue with decorators is accessing arguments of the target function. For example:

	@cache
	def foo(name):
	    pass
		
	@cache
	def bar(id, name):
	    pass
		
Suppose the cache decorator uses the name argument as the cache key. It does have access to the arguments. But they usually come in the forms of \*args and \*\*kw. You have to figure out which one is the "name" by yourself. This is not convenient.

The \_resolve_args method in the Function class will do it for you:

	class cache(Function):
	    def _call(self, *args, **kw):
	        arguments = self._resolve_args(*args, **kw) # the resulting arguments is a dict
	        key = arguments['name']
	        # below is the normal caching logic
	        ...
	        
Multi-level Decorators
----------------------

The situation is even more complicated if the target function is encapsured by multi decorators:

	@cache
	@another_decorator_1
	def foo(name):
	    pass
		
	@cache
	@another_decorator_2
	@another_decorator_3
	def bar(id, name):
	    pass
	    
Now it is extremely difficult for a traditional @cache to get the name argument.
However, if all decorators (@cache, @another\_decorator\_1, @another\_decorator\_2 & @another\_decorator\_3) are derived from the Function class, you won't need to change any code for the cache decorator.

Installtion
===========

pip install decorated

or

easy_install decorated

Decorators
==========

Decorated comes with some common decorators.

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

Loggingd (<a href="https://github.com/CooledCoffee/loggingd" target="_blank">https://github.com/CooledCoffee/loggingd</a>) is a logging framework based on decorated. You can log using decorators.

	from loggingd import log_enter, log_return, log_error
	
	@log_enter('[DEBUG] Calculating {a} / {b} ...')
	@log_return('Result is {ret}.')
	@log_error('[WARN] Failed to calc.', exc_info=True)
	def divide(a, b):
        return a / b
        