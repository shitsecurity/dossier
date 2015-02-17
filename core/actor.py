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

class Signals( object ):

	def invoke( self, *args, **kwargs ): pass

	def shutdown( self, *args, **kwargs ): pass

class Options( object ):

	def __init__( self, *args, **kwargs ):
		super( Options, self ).__init__( *args, **kwargs )
		self._options = {}

	def set_option( self, key, value ):
		self._options[ key ] = value

	def get_option( self, key ):
		return self._options[ key ]

	def configure( self, *args, **kwargs ): pass

class Plugins( dict ):

	def __init__( self, plugins ):
		super( Plugins, self ).__init__([ (_.name,_) for _ in plugins ])
	
	def invoke( self ):
		[ _.invoke() for _ in self.values() ]

	def shutdown( self ):
		[ _.shutdown() for _ in self.values() ]

	def loaded( self, plugin ):
		return plugin in self.keys()

class Actor( Signals, Greenlet ):

	def __init__( self, channels, *args, **kwargs ):
		super( Actor, self ).__init__( *args, **kwargs )
		self.queue = Queue()
		[ channels.setdefault( _, [] ).append( self.queue )
		  for _ in self.listeners ]
		self.channels = channels

	def _run( self ):
		self.act()

class Channels( dict ):

	def publish( self, channel, data ):
		if channel != '*':
			[ _.put(( channel, data )) for _ in self.get('*',[]) ]
		basename = lambda _: '.'.join( _.split('.')[:-1] )
		if channel.endswith('.*'):
			broadcast = channel[:-2]
			for key in self.keys():
				if basename( key ).endswith( broadcast ):
					[ _.put( data ) for _ in self[ key ] ]
		else:
			broadcast = '{}.*'.format( basename(channel) )
			[ _.put( data )
			  for _ in set(chain( self.get( channel, [] ),
				  				  self.get( broadcast, [] ))) ]

class FilterMixin( object ):

	def __init__( self, *args, **kwargs ):
		super( FilterMixin, self ).__init__( *args, **kwargs )
		self.accept_filters = []
		self.reject_filters = []

	def filter_accept( self, lambdaf ):
		self.accept_filters.append( lambdaf )

	def filter_reject( self, lambdaf ):
		self.reject_filters.append( lambdaf )

	def filter( self, *args, **kwargs ):
		if any([_( *args, **kwargs ) for _ in self.reject_filters ]):
			return True

		if self.accept_filters and not all([_( *args, **kwargs )
											for _ in self.accept_filters ]):

			return True
