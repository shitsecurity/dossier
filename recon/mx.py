#!/usr/bin/env python

import dns.name
import dns.resolver

def mx( domain, resolver=None ):
	resolver = resolver or dns.resolver.Resolver()
	dn = dns.name.from_text( str(domain) )
	try:
		names = [ _.to_text().split(' ',1)[1].rstrip('.')
					for _ in resolver.query( dn, 'MX' ) ]
	except( dns.resolver.NXDOMAIN,
			dns.resolver.NoAnswer,
			dns.resolver.NoNameservers ):
		return []
	return names
