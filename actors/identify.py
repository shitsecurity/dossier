#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from who import whois_domain_org, whois_ip_desc

class WhoisDomainActor( Actor ):

	name = 'ns.whois'

	listeners =  [
		'domain.whois',
		'domain.*',
	]

	@forever
	@action
	@unique
	def act( self, domain ):
		orgs = whois_domain_org( domain )
		for org in orgs:
			self.channels.publish( 'whois.domain.org',
									{'domain':domain, 'org':org } )

class WhoisIPActor( Actor ):

	name = 'ip.whois'

	listeners = [
		'ip.whois',
		'ip.*',
	]

	@forever
	@action
	@unique
	def act( self, ip ):
		descs = whois_ip_desc( ip )
		for desc in descs:
			self.channels.publish('whois.ip.desc', {'ip':ip, 'desc':desc })
