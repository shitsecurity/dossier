#!/usr/bin/env python

import logging

from core.log import log as setup_log
from core.actor import Actor, forever, hash

class LogActor( Actor ):

	name = 'log'

	listeners =  [ '*', ]

	def __init__( self, *args, **kwargs ):
		super( LogActor, self ).__init__( *args, **kwargs )
		setup_log()
		self.cache = set()

	@forever
	def act( self ):
		(channel,data) = self.queue.get()
		hashed = hash( data )
		if hashed in self.cache: return
		self.cache.add( hashed )
		if channel.startswith('map.'): return
		logging.debug( '{channel} | {data}'.format( channel=channel.upper(),
													data = data ))

class FileActor( Actor ):

	name = 'file'

	listeners =  [ '*', ]

	def __init__( self, *args, **kwargs ):
		super( FileActor, self ).__init__( *args, **kwargs )
		self.cache = set()
		self.file = 'results'

		self.map = []
		self.port = []
		self.rank = []

	@forever
	def act( self ):
		(channel,data) = self.queue.get()

		if channel == 'signal' and data == 'shutdown':
			self.save_results()
			return

		elif channel == 'opt.file':
			self.file = data
			return

		hashed = hash( data )
		if hashed in self.cache: return
		self.cache.add( hashed )

		type = channel.split('.')[0]
		if type == 'map' and channel == 'map.domain_ip':
			self.map.append('{} {}'.format( data.get('ip'),
											data.get('domain') ))
		elif type == 'rank':
			engine = channel.split('.')[1]
			self.rank.append('{} {} {}'.format( engine,
												data.get('domain'),
												data.get('rank') ))
		elif type == 'port':
			self.port.append('{} {}'.format(data.get('ip'),
											data.get('port')))

	def save_results( self ):
		with open( self.file, 'wb+' ) as fh:
			[ fh.write( '\n'.join( _ ) ) for _ in [ self.map,
													self.rank,
													self.port ] ]
