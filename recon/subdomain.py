#!/usr/bin/env python

import os

from a import a
from any import any

from diff import Differ
from utils import hld

import http

from resolver import Resolver
from session import Session

class Subdomain( object ):

    def __init__( self, tld, ratio=0.95, error_valid=True ):
        self.tld = tld
        self.ratio = ratio
        self.error_valid = error_valid
        self.wildcard = is_wildcard( tld )
        if self.wildcard:
            self.baseline = http.fetch('{subdomain}.{domain}' \
                                        .format(subdomain=rand_subdomain(),
                                                domain=tld))
            self.session = Session()
        else:
            self.resolver = Resolver()

    def brute( self, subdomain ):
        fqdn = '{}.{}'.format( subdomain, self.tld )
        if self.wildcard:
            return brute( fqdn,
                          wildcard=self.wildcard,
                          baseline=self.baseline,
                          session=self.session,
                          error_valid=self.error_valid,
                          ratio=self.ratio )
        else:
            return brute( fqdn,
                          wildcard=self.wildcard,
                          resolver=self.resolver,
                          ratio=self.ratio )

    def exists( self, *args, **kwargs ):
        return len( self.brute( *args, **kwargs ) ) > 0

def load( file ):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        '..',
                        'data',
                        file )
    with open(path,'rb') as fh:
        return [ _.strip() for _ in fh.readlines() ]

def subdomains( wordlist='subdomains.wl' ):
    return load( wordlist )

def is_simular( baseline, test, ratio, differ=None ):
    differ = differ or Differ( baseline, test )
    if differ.ratio() >= ratio:
        return True
    else:
        return False

def brute( subdomain,
           wildcard=False,
           resolver=None,
           session=None,
           baseline=None,
           error_valid=True,
           ratio=0.95 ):

    if wildcard == False: return any( domain=subdomain, resolver=resolver )

    if baseline is None:
        try:
            url = '{}.{}'.format( rand_subdomain(), hld(subdomain) )
            baseline = http.fetch( url, session=session)
        except http.ConnectionError:
            baseline=None

    try:
        new = http.fetch( subdomain, session=session )

    except http.ConnectionError:

        if baseline is None or error_valid == True:
            return [ subdomain, ]
        else:
            return []

    if is_simular( baseline, new, ratio ):
        return []
    else:
        return [ subdomain, ]

def rand_subdomain():
    return os.urandom(8).encode('hex')

def is_wildcard( domain, resolver=None ):
    subdomain = rand_subdomain()
    domain = '{subdomain}.{domain}'.format( subdomain=subdomain, domain=domain )
    if len( a( domain, resolver ) ) > 0:
        return True
    else:
        return False
