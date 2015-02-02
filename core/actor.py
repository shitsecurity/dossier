#!/usr/bin/env python

from gevent import Greenlet, wait
from gevent.queue import Queue

from functools import wraps
from itertools import chain

import mmh3

def forever( f ):
	@wraps( f )
	def wrapper( *args, **kwargs ):
		while True:
			f( *args, **kwargs )
	return wrapper

def action( f ):
	@wraps( f )
	def wrapper( self, *args, **kwargs ):
		data = self.queue.get()
		return f( self, data, *args, **kwargs )
	return wrapper

def hash( data ):
	return mmh3.hash( str(data) )

def unique( f ):
	cache = set()
	@wraps( f )
	def wrapper( self, data, *args, **kwargs ):
		hashed = hash( data )
		if hashed not in cache:
			cache.add( hashed )
			return f( self, data, *args, **kwargs )
	return wrapper

class Actor( Greenlet ):

	def __init__( self, channels, **kwargs ):
		super( Actor, self ).__init__()
		self.queue = Queue()
		[ channels.setdefault( x, [] ).append( self.queue )
		  for x in self.listeners ]
		self.channels = channels

	def _run( self ):
		self.act()

class Channels( dict ):

	def publish( self, channel, data ):
		if channel != '*':
			[ x.put(( channel, data )) for x in self[ '*' ] ]
		basename = lambda x: '.'.join( x.split('.')[:-1] )
		if channel.endswith('.*'):
			broadcast = channel[:-2]
			for key in self.keys():
				if basename( key ).endswith( broadcast ):
					[ x.put( data ) for x in self[ key ] ]
		else:
			broadcast = '{}.*'.format( basename(channel) )
			[ x.put( data )
			  for x in set(chain( self.get( channel, [] ),
				  				  self.get( broadcast, [] ))) ]
