#!/usr/bin/env python

def spawn( plugins, *args, **kwargs ):
	return [ _.spawn(*args,**kwargs) for _ in plugins ]
