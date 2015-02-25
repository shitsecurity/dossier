#!/usr/bin/env python

from core.actor import Actor, forever, action, unique, Options

from subnet import ip_find as find

from iptools import IpRange

class SubnetActor( Options, Actor ):

	name = 'ip.subnet'

	listeners =  [
		'ip.subnet',
	]

	def __init__( self, *args, **kwargs ):
		super( SubnetActor, self ).__init__( *args, **kwargs )
		self.ignore = []
		self.set_option('mask',24)
		self.set_option('threads',10)

	def configure( self, config ):
		if config.has_option(self.name, 'mask'):
			self.set_option('mask', config.getint(self.name, 'mask'))
		if config.has_option(self.name, 'threads'):
			self.set_option('threads', config.getint(self.name, 'threads'))

	@forever
	@action
	def act( self, ip ):
		for ignore_range in self.ignore:
			if ip in ignore_range:
				return
		mask = self.get_option('mask')
		concurrency = self.get_option('threads')
		self.ignore.append(IpRange('{ip}/{mask}'.format(ip=ip,mask=mask)))
		[ self.channels.publish( 'ip.*', _ )
		for _ in find( ip, mask=mask, concurrency=concurrency ) ]
