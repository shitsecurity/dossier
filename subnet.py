#!/usr/bin/env python

from core import concurrency
from core.pool import Pool

from recon.ptr import ptr, verify as verify_domain
from recon.subnet import subnet
from recon.resolver import Resolver
from recon.utils import all_dns

from functools import partial

from iptools import IpRange

def find( ip, 
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
	#mapping = {}
	#for target in ip_range:
		#for domain in ptr(target,resolver=resolver):
			#if not verify or verify_domain(target,domain,resolver=resolver):
				#domains = mapping.setdefault(target,[])
				#domains += filter(in_subnet,all_dns(domain))
	#return mapping
	mapping = []
	pool = pool or Pool(10)
	def lookup( target ):
		for domain in ptr( target, resolver=resolver ):
			if not verify or verify_domain( target, domain, resolver=resolver ):
				return (target,filter( in_subnet, all_dns( domain )))
	return dict([(k,v) for (k,v) in filter(None,pool.map(lookup,ip_range))])
