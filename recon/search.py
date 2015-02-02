#!/usr/bin/env python

import http
import lxml.html
import urlparse
import iptools.ipv4 as ipv4
import iptools.ipv6 as ipv6
import re

from http import Session

def bing_domains( ip, session=None ):

	url = 'http://www.bing.com/search?q={}'
	ip = 'ip:{}'.format( ip )
	dn = ' -{}'
	domains = []

	while True:

		exclude = ''.join([ dn.format( _ ) for _ in domains ])

		data = http.fetch( url.format( ip+exclude ), session=session )

		xml = lxml.html.fromstring( data )
		netloc = lambda _: urlparse.urlparse( _.get('href') ).netloc
		uniq_links = set([ netloc( el ) for el in xml.xpath('//h2/a') ])
		domains += uniq_links
		
		next_page = len( xml.xpath('//nav/ul/li/a[text()=2]') )>0
		if not next_page:
			break

	is_domain = lambda _: False if ipv4.validate_ip(_) or ipv6.validate_ip(_) \
						  else True 
	return filter( is_domain, domains )

class BannedByGoogle( Exception ): pass

def google_subdomains( domain, session=None ):

	url = 'http://www.google.com/search?q={}'
	domain = 'site:{}'.format( domain )
	dn = ' -{}'
	domains = []

	strip = lambda _: _.replace('<b>','').replace('</b>','').replace('"','')
	normalize = lambda _: _ if _.startswith('http') else 'http://{}'.format( _ )
	netloc = lambda _: urlparse.urlparse( _ ).netloc
	limit = lambda _: True if len(_.split(' ')) > 11 else False

	banned_str ='Our systems have detected unusual traffic '\
				'from your computer network.'
	banned_re = re.compile(re.escape( banned_str ))
	banned = lambda _: True if banned_re.search(_) else False

	while True:

		exclude = ''.join([ dn.format( _ ) for _ in domains ])

		#print '[*] requesting {}'.format( url.format( domain+exclude ))
		data = http.fetch( url.format( domain+exclude ), session=session )

		if banned(data):
			raise BannedByGoogle()

		xml = lxml.html.fromstring( data )
		uniq_links = list(set([ netloc(normalize(strip( _.text )))
								for _ in xml.xpath('//div/cite') ]))
		domains += uniq_links
		#print '[+] {}'.format( ' '.join( uniq_links ))

		next_page = len( xml.xpath('//tr/td/a[text()=2]') )>0
		if not next_page or limit( domain+exclude ):
			break

	return domains
