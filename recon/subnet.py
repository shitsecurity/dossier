#!/usr/bin/env python

import dns.name

def subnet( domains, domain ):
	domain = dns.name.from_text( domain )
	test = lambda _: _.is_superdomain( domain ) or _.is_subdomain( domain )
	if len(filter( test, [ dns.name.from_text(_) for _ in domains ])) > 0:
		return True
	else:
		return False
