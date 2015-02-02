#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from portscan import syn, tcp_ports

class SynScanActor( Actor ):

	name = 'scan.syn'

	listeners =  [
		'scan.syn',
		'ip.*',
	]

	def __init__( self, *args, **kwargs ):
		super( SynScanActor, self ).__init__( *args, **kwargs )
		self.ports = tcp_ports()

	@forever
	@action
	@unique
	def act( self, ip ):
		ports = syn( ip, self.ports )
		[ self.channels.publish('port.*', {'ip':ip,'port':x}) for x in ports ]
