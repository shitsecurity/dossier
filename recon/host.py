#!/usr/bin/env python

import re
import json

from recon.a import a
from recon.ptr import ptr
from recon.http import fetch

from http import Session

def dnsdigger( host ):
	url = 'http://www.dnsdigger.com/'
	token_url = url 
	query_url = url + 'hostcollision.php?host={host}&token={token}'
	session=Session()
	token = re.search( 'name="token"\svalue="(?P<token>.*?)">',
						fetch( token_url, session=session ),
						re.U & re.M ).group('token')
	names = re.findall('<a\shref=".*?"\srel="nofollow">(.*?)</a>',
						fetch( query_url.format( token=token, host=host ),
								session=session,
								headers={'Referer': url} ),
						re.U and re.M )
	return names

def yougetsignal( host ):
	query_url = 'http://domains.yougetsignal.com/domains.php'
	data = { 'remoteAddress': host, 'key': '' }
	headers = { 'X-Requested-With': 'XMLHttpRequest',
				'X-Prototype-Version': '1.6.0',
				'Referer': 'http://www.yougetsignal.com/tools/'
							'web-sites-on-web-server/',
				'User-Agent': 'Mozilla/5.0'	}
	results = json.loads( fetch(query_url, 
								method='post', 
								data=data, 
								headers=headers))
	return [ _[0] for _ in results['domainArray'] ]

def verify( domain, ips, engine=a, resolver=None ):
	'''verify at least one ip resolves to domain name
	>>> verify( 'google.com', a('google.com') )
	True
	'''
	if len(set(ips).intersection(engine( domain, resolver=resolver )))>0:
		return True
	else:
		return False

def reverse_dns( host, engine=dnsdigger ):
	return engine( host )
