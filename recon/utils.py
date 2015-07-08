#!/usr/bin/env python

import dns.name

def all_dns( domain ):
    '''
    >>> all_dns('www.google.com')
    ['www.google.com', 'google.com']
    '''
    all = []
    name = dns.name.from_text( str(domain) )
    level = len(name.labels)
    for i in range( 0, level-2 ):
        dn = ".".join( name.labels[i:] )[:-1]
        all.append( dn )
    return all

def hld( subdomain ):
    '''
    >>> hld('www.google.com')
    'google.com'
    '''
    return '.'.join( dns.name.from_text(subdomain).labels[1:] ).rstrip('.')

def unique( f ):
    @wraps( f )
    def wrapper( *args, **kwargs ):
        return list(set(f( *args, **kwargs )))
    return wrapper
