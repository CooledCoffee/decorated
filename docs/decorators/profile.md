# Profile

	from decorated import profile
	
	@profile(iterations=100)
	def heavy_calc():
	    pass
	
	heavy_calc()
	
This profiles the function using cProfile.
The result is written to stdout.
You can also use the LOGGING_REPORTER to write the result to logging.
Refer to [timeit](timeit.md) for more information.
