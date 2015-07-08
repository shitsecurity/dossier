#!/usr/bin/env python

from core import concurrency
from core.pool import Pool

from recon.subdomain import Subdomain, subdomains, subdomains as load_subdomains

from itertools import ifilter

def brute( domain, subdomains=None, pool=None, concurrency=10 ):
    domain = Subdomain( domain )
    subdomains = subdomains or load_subdomains()
    pool = pool or Pool(concurrency)
    return ifilter(None, pool.imap( lambda _: _ if domain.exists(_) else None,
                                    subdomains ))
