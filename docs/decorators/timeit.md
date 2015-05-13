# Timeit

	from decorated import timeit
	
	@timeit(iterations=100, repeats=3)
	def heavy_calc():
	    pass
	
	heavy_calc()
	
This example executes heavy\_calc 100 times and measure the execution time.
It repeats this process 3 times and then write the result to stdout.
You can also write to loggind by specifying reporter=LOGGING_REPORTER.

	from decorated import timeit
	from decorated.util.reporters import LOGGING_REPORTER
	
	@timeit(iterations=100, repeats=3, reporter=LOGGING_REPORTER)
	def heavy_calc():
	    pass
	
	heavy_calc()
