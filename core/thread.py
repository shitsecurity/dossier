#!/usr/bin/env python

def spawn( plugins, *args, **kwargs ):
	return [ x.spawn(*args,**kwargs) for x in plugins ]

def start( greenlets ):
	return [ x.start() or x for x in greenlets ]
