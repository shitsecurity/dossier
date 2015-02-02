#!/usr/bin/env python

from recon.a import aaaa, a

from recon.soa import soa
from recon.ns import ns
from recon.mx import mx
from recon.srv import srv

from recon.cname import cname

from recon.resolver import Resolver

from recon.ptr import ptr, verify as verify_ip
from recon.utils import all_dns

from recon.host import reverse_dns as reverse_dns_unverified
from recon.host import dnsdigger, yougetsignal
from recon.host import verify as verify_dns

from functools import partial

from recon.search import bing_domains
from recon.search import google_subdomains

from recon.search import Session

def lookup( domain, *args, **kwargs ):
	return a( domain, *args, **kwargs )

def lookupv4( domain, *args, **kwargs ):
	return a( domain, *args, **kwargs )

def lookupv6( domain, *args, **kwargs ):
	return aaaa( domain, *args, **kwargs )

def meta( domain, *args, **kwargs ):
	names = set()
	[names.update(x(domain,*args,**kwargs)) for x in [soa,ns,mx,srv,cname]]
	return list(names)

def reverse_ip( ip, *args, **kwargs ):
	names = set()
	[ names.update( all_dns(x) )
	  for x in ptr( ip, *args, **kwargs )
	  if verify_ip( ip, x ) ]
	return list(names)

def reverse_dns( domain, *args, **kwargs ):
	names = set()
	ips = a(domain,*args,**kwargs)
	names.update([x.lstrip('www.') for x in
				  filter(partial(verify_dns,
					  			 ips=ips,
					  			 *args,
								 **kwargs),
						 reverse_dns_unverified(domain,engine=dnsdigger))])
	return list(names)

def domains( host, *args, **kwargs ):
	names = set()
	domains = bing_domains( host, *args, **kwargs )
	return list(domains)

def subdomains( domain, *args, **kwargs ):
	names = set()
	subdomains = google_subdomains( domain, *args, **kwargs )
	return list(subdomains)
