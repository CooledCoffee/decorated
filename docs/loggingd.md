# Loggingd

<a href="https://github.com/CooledCoffee/loggingd" target="_blank">Loggingd</a> is a logging framework based on decorated.

	from loggingd import log_enter, log_return, log_error
	
	@log_enter('[DEBUG] Calculating {a} / {b} ...')
	@log_return('Result is {ret}.')
	@log_error('[WARN] Failed to calc.', exc_info=True)
	def divide(a, b):
        return a / b
        