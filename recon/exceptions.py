#!/usr/bin/env python

from functools import wraps

def safe( exception, error=lambda: None ):
	def decorator( f ):
		@wraps( f )
		def wrapper( *args, **kwargs ):
			try:
				return f( *args, **kwargs )
			except exception:
				return error()
		return wrapper
	return decorator
