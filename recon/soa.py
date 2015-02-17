#!/usr/bin/env python

import dns.name
import dns.resolver

def soa( domain, resolver=None ):
	resolver = resolver or dns.resolver.Resolver()
	dn = dns.name.from_text( str(domain) )
	try:
		names = [ _.to_text() for _ in resolver.query( dn, 'SOA' )]
	except( dns.resolver.NXDOMAIN, 
			dns.resolver.NoAnswer,
			dns.resolver.NoNameservers ):
		return []
	names = reduce( lambda ctx, ii: ctx + [ _.rstrip('.')
											for _ in ii.split(' ')[0:2] ],
					names,
					[] )
	return names
