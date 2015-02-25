#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from ns import lookup, meta, Resolver, reverse_dns, reverse_ip
from ns import domains, Session, subdomains

class NSLookupActor( Actor ):

	name = 'ns.lookup'

	listeners =  [
		'domain.*',
		'domain.lookup',
		'domain.lookup.*'
	]

	def __init__( self, *args, **kwargs ):
		super( NSLookupActor, self ).__init__( *args, **kwargs )
		self.resolver = Resolver()

	@forever
	@action
	@unique
	def act( self, domain ):
		names = lookup( domain, resolver=self.resolver )
		[ self.channels.publish('ip.*', _ ) for _ in names ]
		[ self.channels.publish( 'map.domain_ip',
								{'domain':domain,'ip': _ }) for _ in names ]

class NSExtendedActor( Actor ):

	name = 'ns.ext'

	listeners = [
		'domain.ext',
		'domain.lookup.*'
	]

	def __init__( self, *args, **kwargs ):
		super( NSExtendedActor, self ).__init__( *args, **kwargs )
		self.resolver = Resolver()

	@forever
	@action
	@unique
	def act( self, domain ):
		names = meta( domain, resolver=self.resolver )
		[ self.channels.publish('domain.lookup', _ ) for _ in names ]

class ReverseNSActor( Actor ):

	name = 'ns.reverse'

	listeners = [
		'domain.reverse_dns', #'ip.reverse_dns',
	]

	def __init__( self, *args, **kwargs ):
		super( ReverseNSActor, self ).__init__( *args, **kwargs )
		self.resolver = Resolver()

	@forever
	@action
	@unique
	def act( self, domain ):
		names = reverse_dns( domain, resolver=self.resolver )
		[ self.channels.publish('domain.lookup.*', _) for _ in names ]

class ReverseIPActor( Actor ):

	name = 'ip.reverse'

	listeners = [
		'ip.*',
		'ip.reverse_ip',
	]

	def __init__( self, *args, **kwargs ):
		super( ReverseIPActor, self ).__init__( *args, **kwargs )
		self.resolver = Resolver()

	@forever
	@action
	@unique
	def act( self, ip ):
		names = reverse_ip( ip, resolver=self.resolver )
		[ self.channels.publish('domain.lookup.*', _ ) for _ in names ]

class BingIPActor( Actor ):

	name = 'ip.bing'

	listeners = [
		'ip.*',
		'ip.bing',
	]

	def __init__( self, *args, **kwargs ):
		super( BingIPActor, self ).__init__( *args, **kwargs )
		self.session = Session()

	@forever
	@action
	@unique
	def act( self, ip ):
		names = domains( ip, session=self.session )
		[ self.channels.publish('domain.lookup.*', _ ) for _ in names ]

class GoogleNSActor( Actor ):

	name = 'ns.google'

	listeners = [
		'domain.google',
	]

	def __init__( self, *args, **kwargs ):
		super( GoogleNSActor, self ).__init__( *args, **kwargs )
		self.session = Session()

	@forever
	@action
	@unique
	def act( self, domain ):
		names = subdomains( domain, session=self.session )
		[ self.channels.publish('domain.lookup.*', _ ) for _ in names ]
