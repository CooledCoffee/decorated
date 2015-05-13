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

&nbsp;&nbsp;&nbsp;&nbsp;2\.1\. [Accessing target function arguments](docs/advanced/arguments.md)

&nbsp;&nbsp;&nbsp;&nbsp;2\.2\. [Chaining decorators](docs/advanced/chaining.md)

&nbsp;&nbsp;&nbsp;&nbsp;2\.3\. [Decorators on class methods](docs/advanced/method.md)

&nbsp;&nbsp;&nbsp;&nbsp;2\.4\. [Wrapper Decorator](docs/advanced/wrapper.md)

3\. Built-in decorators

&nbsp;&nbsp;&nbsp;&nbsp;3\.1\. [cache](docs/decorators/cache.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.2\. [conditional](docs/decorators/conditional.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.3\. [events](docs/decorators/events.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.4\. [once](docs/decorators/once.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.5\. [profile](docs/decorators/profile.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.6\. [remove\_extra\_args](docs/decorators/remove_extra_args.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.7\. [retries](docs/decorators/retries.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.8\. [synchronized](docs/decorators/synchronized.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.9\. [timeit](docs/decorators/timeit.md)

&nbsp;&nbsp;&nbsp;&nbsp;3\.10\. [timeout](docs/decorators/timeout.md)

4\. [Loggingd](docs/loggingd.md)
