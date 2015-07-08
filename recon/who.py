#!/usr/bin/env python

from whois import whois
from ipwhois import IPWhois

import re

from functools import wraps

from exceptions import safe

def whois_domain( domain ):
    return whois( domain ).text.split('\n')

def unique( f ):
    @wraps( f )
    def wrapper( *args, **kwargs ):
        return list(set(f( *args, **kwargs )))
    return wrapper

@safe( TypeError )
@unique
@safe( IndexError )
def whois_domain_org( domain ):
    regex = re.compile('organization:\s+(.*)', re.I)
    return [m.groups(1)[0] for m in
            filter(None, [regex.search(_) for _ in whois_domain(domain)] )]

def whois_ip( ip ):
    return IPWhois( ip ).lookup()

@safe( KeyError )
@safe( TypeError )
def whois_ip_desc( ip ):
    return [ _['description'] for _ in whois_ip(ip)['nets'] ]
