# Chaining decorators

You can wrap a function with multiple decorators like this:

	@decorator2
	@decorator1
	def foo(a, b, c):
	    pass

This behavior is supported by standard python decorators.
However, accessing the arguments from within "decorator2" is a little crumsy.
Decorated solves this problem by providing a unified \_resolve\_args method (see [Accessing target function arguments](arguments.md)).
