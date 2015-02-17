#!/usr/bin/env python

from core.actor import Actor, forever, action, unique, Options

from portscan import syn, tcp_ports, udp, udp_ports

class SynScanActor( Options, Actor ):

	name = 'scan.syn'

	listeners =  [
		'scan.syn',
		'ip.*',
	]

	def __init__( self, *args, **kwargs ):
		super( SynScanActor, self ).__init__( *args, **kwargs )
		self.set_option('ports','ports.yaml')

	def configure( self, config ):
		if config.has_option(self.name, 'ports'):
			self.set_option('ports', config.get(self.name, 'ports'))

	def invoke( self ):
		self.ports = tcp_ports( self.get_option('ports') )

	@forever
	@action
	@unique
	def act( self, ip ):
		ports = syn( ip, self.ports )
		[self.channels.publish('port.tcp.*',{'ip':ip,'port':_}) for _ in ports]

class UDPScanActor( Options, Actor ):

	name = 'scan.udp'

	listeners =  [
		'scan.udp',
		'ip.*',
	]

	def __init__( self, *args, **kwargs ):
		super( UDPScanActor, self ).__init__( *args, **kwargs )
		self.set_option('ports','ports.yaml')

	def configure( self, config ):
		if config.has_option(self.name, 'ports'):
			self.set_option('ports', config.get(self.name, 'ports'))

	def invoke( self ):
		self.ports = udp_ports( self.get_option('ports') )

	@forever
	@action
	@unique
	def act( self, ip ):
		ports = udp( ip, self.ports )
		[self.channels.publish('port.udp.*',{'ip':ip,'port':_}) for _ in ports]
