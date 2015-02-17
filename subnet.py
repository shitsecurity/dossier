#!/usr/bin/env python

from core import concurrency
from core.pool import Pool

from recon.ptr import ptr, verify as verify_domain
from recon.subnet import subnet
from recon.resolver import Resolver
from recon.utils import all_dns

from functools import partial

from iptools import IpRange

from itertools import ifilter

def iter_find( ip,
				context=None,
				mask=24,
				verify=False,
				resolver=None,
				pool=None,
				concurrency=10 ):

	resolver = resolver or Resolver()
	pool = pool or Pool(concurrency)
	context = context or [] # always passed in
	for domain in ptr( ip, resolver=resolver ):
		if not verify or verify_domain( ip, domain, resolver=resolver ):
			context += all_dns( domain )
	in_subnet = partial( subnet, context )
	ip_range = IpRange('{ip}/{mask}'.format( ip=ip, mask=mask ))
	mapping = []
	pool = pool or Pool(10)
	def lookup( target ):
		for domain in ptr( target, resolver=resolver ):
			if not verify or verify_domain( target, domain, resolver=resolver ):
				return ( target, filter( in_subnet, all_dns( domain )))
	return ifilter( None, pool.imap( lookup, ip_range ))

def find( *args, **kwargs ):
	return dict([(k,v) for (k,v) in iter_find( *args, **kwargs )])

def ip_stream( iter ):
	for _ in iter:
		yield _[0]

def ip_find( *args, **kwargs ):
	for ip in ip_stream( iter_find( *args, **kwargs )):
		yield ip
