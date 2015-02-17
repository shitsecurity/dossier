#!/usr/bin/env python

import logging

from core.log import log as setup_log
from core.actor import Actor, forever, hash, FilterMixin, Options

class LogActor( Actor ):

	name = 'verbose'

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

class FileActor( Options, FilterMixin, Actor ):

	name = 'report'

	listeners =  [ '*', ]

	def __init__( self, *args, **kwargs ):
		super( FileActor, self ).__init__( *args, **kwargs )
		self.cache = set()
		self.set_option('file','results')

	def configure( self, config ):
		if config.has_option(self.name, 'file'):
			self.set_option('file', config.get(self.name, 'file'))
		
	def invoke( self ):
		self.fh = open( self.get_option('file'), 'wb+' )

	def shutdown( self ):
		self.fh.close()

	@forever
	def act( self ):
		(channel,data) = self.queue.get()

		if self.filter( channel, data ):
			return

		hashed = hash( data )
		if hashed in self.cache: return
		self.cache.add( hashed )

		type = channel.split('.')[0]

		if type == 'map':
			self.fh.write('MAP {} {}\n'.format( data.get('ip'),
												data.get('domain') ))

		elif type == 'ip':
			self.fh.write('IP {}\n'.format( data ))

		elif type == 'domain':
			self.fh.write('DOMAIN {}\n'.format( data ))

		elif type == 'rank':
			engine = channel.split('.')[1]
			self.fh.write('RANK.{} {} {}\n'.format( engine.upper(),
													data.get('domain'),
													data.get('rank')) )

		elif type == 'port':
			proto = channel.split('.')[1]
			self.fh.write('PORT.{} {} {}\n'.format( proto,
													data.get('ip'),
													data.get('port')) )

		elif type == 'geoip':
			self.fh.write( 'GEOIP {} {}\n'.format( data.get('ip'),
													data.get('country') ))

		elif type == 'whois':
			key_type, key_data = channel.split('.')[1:3]
			self.fh.write('WHOIS.{} {} {}\n'.format(key_type.upper(),
													data.get(key_type),
													data.get(key_data) ))
