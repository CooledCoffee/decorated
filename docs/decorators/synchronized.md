# Synchronized

The effect of @synchronized is similar to its counter-part in java.
For example,

	from decorated import synchronized
	from decorated.decorators.synchronized import MemoryLock
	
	lock = MemoryLock()
	
	@synchronized(lock)
	def save_to_db_1():
	    pass
	    
	@synchronized(lock)
	def save_to_db_2():
	    pass

The executions of save\_to\_db\_1 and save\_to\_db\_2 are synchronized to prevent conflict.
You can switch from MemoryLock to FileLock (only works on linux) to synchronize among multi processes.
You can also implement distributed locks using ZooKeeper.
