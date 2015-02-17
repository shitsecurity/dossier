#!/usr/bin/env python

import http
import lxml.html
import urlparse
import iptools.ipv4 as ipv4
import iptools.ipv6 as ipv6
import re
import logging

from http import Session

def bing_domains( ip, session=None ):

	url = 'http://www.bing.com/search?q={}'
	ip = 'ip:{}'.format( ip )
	dn = ' -{}'
	domains = []

	while True:

		exclude = ''.join([ dn.format( _ ) for _ in domains ])

		try:
			uri = url.format( ip+exclude )
			data = http.fetch( uri, session=session )
		except http.Timeout, http.ConnectionError:
			logging.error('cannot fetch bing @{}'.format( uri ))
			break
		if data=='':
			logging.error('null response by bing @{}'.format( ip ))
			break
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
	encode = lambda _: _.encode('utf-8')

	while True:

		exclude = ''.join([ dn.format( _ ) for _ in domains ])

		#print '[*] requesting {}'.format( url.format( domain+exclude ))
		try:
			uri = url.format( domain+exclude )
			data = http.fetch( uri, session=session )
		except http.Timeout, http.ConnectionError:
			logging.error('cannot fetch google @{}'.format( uri ))
			break

		if banned(data):
			logging.error('banned by google @{}'.format( domain ))
			#raise BannedByGoogle()
			break

		elif data=='':
			logging.error('null response by google @{}'.format( domain ))

		xml = lxml.html.fromstring( data )
		uniq_links = list(set([ netloc(normalize(strip(encode( _.text ))))
								for _ in xml.xpath('//div/cite') ]))
		domains += uniq_links
		#print '[+] {}'.format( ' '.join( uniq_links ))

		next_page = len( xml.xpath('//tr/td/a[text()=2]') )>0
		if not next_page or limit( domain+exclude ):
			break

	return domains
