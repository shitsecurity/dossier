#!/usr/bin/env python

from recon.a import a

import dns.reversename
import dns.resolver
import dns.exception

def ptr( ip, resolver=None ):
    resolver = resolver or dns.resolver.Resolver()
    rip = dns.reversename.from_address(ip)
    try:
        names = resolver.query( rip, 'PTR' )
    except( dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers ):
        return []
    return [ _.to_text() for _ in names ]

def verify( ip, domain, engine=a, resolver=None ):
    '''verify domain resolves to ip address
    >>> verify( '8.8.8.8', ptr('8.8.8.8')[0] )
    True
    '''
    if ip in engine( domain, resolver=resolver ):
        return True
    else:
        return False
