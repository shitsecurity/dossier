#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from subnet import find

from iptools import IpRange

class SubnetActor( Actor ):

	name = 'ip.subnet'

	listeners =  [
		'ip.subnet',
	]

	def __init__( self, mask=24, *args, **kwargs ):
		super( SubnetActor, self ).__init__( *args, **kwargs )
		self.ignore = []
		self.mask = mask

	@forever
	@action
	def act( self, ip ):
		for ignore_range in self.ignore:
			if ip in ignore_range:
				return
		self.ignore.append(IpRange('{ip}/{mask}'.format(ip=ip,mask=self.mask)))
		mapping = find( ip, mask=self.mask )
		[ self.channels.publish('ip.in_subnet',x) for x in mapping.iterkeys() ]
