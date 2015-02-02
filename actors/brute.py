#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from subdomains import subdomains, brute as brute_subdomains

from itertools import chain

class SubdomainsActor( Actor ):

	name = 'subdomains.brute'

	listeners =  [
		'subdomains.brute',
		'domain.brute',
	]

	def __init__( self, *args, **kwargs ):
		super( SubdomainsActor, self ).__init__( *args, **kwargs )
		self.subdomains = subdomains()

	@forever
	@action
	@unique
	def act( self, domain ):
		subdomains = brute_subdomains( domain, self.subdomains )
		domains = [ '{}.{}'.format( x, domain ) for x in subdomains ]
		[ self.channels.publish('domain.lookup.subdomain', x) for x in domains ]
