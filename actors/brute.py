#!/usr/bin/env python

from core.actor import Actor, forever, action, unique, Options

from subdomains import subdomains, brute as brute_subdomains

from itertools import chain

class SubdomainsActor( Options, Actor ):

	name = 'ns.brute'

	listeners =  [
		'subdomains.brute',
		'domain.brute',
	]

	def __init__( self, *args, **kwargs ):
		super( SubdomainsActor, self ).__init__( *args, **kwargs )
		self.set_option('threads',10)
		self.set_option('wordlist','subdomains.wl')

	def configure( self, config ):
		if config.has_option(self.name, 'threads'):
			self.set_option('threads', config.getint(self.name, 'threads'))
		if config.has_option(self.name, 'wordlist'):
			self.set_option('wordlist', config.get(self.name, 'wordlist'))

	def invoke( self ):
		self.subdomains = subdomains( self.get_option('wordlist') )

	@forever
	@action
	@unique
	def act( self, domain ):
		concurrency=self.get_option('threads')
		subdomains = brute_subdomains( domain,
										self.subdomains,
										concurrency=concurrency )
		[ self.channels.publish('domain.lookup.subdomain',
								'{}.{}'.format(_,domain) ) for _ in subdomains ]
