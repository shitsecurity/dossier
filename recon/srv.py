#!/usr/bin/env python

import dns.name
import dns.resolver

def srv( domain, resolver=None ):
    resolver = resolver or dns.resolver.Resolver()
    dn = dns.name.from_text( str(domain) )
    try:
        names = [ _.to_text() for _ in resolver.query( dn, 'SRV' ) ]
    except( dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers ):
        return []
    return names
