#!/usr/bin/env python

from core import concurrency
from core.pool import Pool

from recon.subdomain import Subdomain, subdomains, subdomains as load_subdomains

def brute( domain, subdomains=None, pool=None, concurrency=10 ):
	domain = Subdomain( domain )
	subdomains = subdomains or load_subdomains()
	pool = pool or Pool(concurrency)
	return filter( None, pool.map( lambda x: x if domain.exists(x) else None,
									subdomains ))
