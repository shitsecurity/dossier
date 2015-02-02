#!/usr/bin/env python

import dns.name

def subnet( domains, domain ):
	domain = dns.name.from_text( domain )
	test = lambda x: x.is_superdomain( domain ) or x.is_subdomain( domain )
	if len(filter( test, [ dns.name.from_text(x) for x in domains ])) > 0:
		return True
	else:
		return False
