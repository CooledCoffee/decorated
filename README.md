Python decorators are very powerful but sometimes a little tricky to write
Decorators themself could be implemented as functions or classes.
Some decorators should be called with arguments, some are not, and some can be used with or without arguments.
It is useful to get the arguments of the target function in the decorators.
But figuring out which aregument is for which parameter is not an easy task.
Things get even messier when you try to wrap a function with multiple decorators.

This is where decorated comes to rescue.
Decorated solves all the above problems by providing a unified framework for writing decorators.
It also provides some built-in decorators that you may find helpful to your daily work.

1\. [Basic](docs/basic.md)

2\. Advanced

2\.1\. [Accessing target function arguments](docs/advanced/arguments.md)

2\.2\. [Chaining decorators](docs/advanced/chaining.md)

2\.3\. [Decorators on class methods](docs/advanced/method.md)

2\.4\. [Wrapper Decorator](docs/advanced/wrapper.md)

3\. Built-in decorators

3\.1\. [cache](docs/decorators/cache.md)

3\.2\. [conditional](docs/decorators/conditional.md)

3\.3\. [events](docs/decorators/events.md)

3\.4\. [once](docs/decorators/once.md)

3\.5\. [remove\_extra\_args](docs/decorators/remove_extra_args.md)

3\.6\. [retries](docs/decorators/retries.md)

3\.7\. [synchronized](docs/decorators/synchronized.md)

3\.8\. [timeout](docs/decorators/timeout.md)

4\. [Loggingd](docs/loggingd.md)
