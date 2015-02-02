#!/usr/bin/env python

from requests import Session
from requests.exceptions import Timeout

def hash( domain ):
	seed = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE."\
			"Yes, I'm talking to you, scammer."
	hash = 0x01020345
	for i in range( len( domain )):
		hash = hash ^ ord( seed[ i % len( seed ) ]) ^ ord( domain[ i ] )
		hash = hash >> 23 | hash << 9
		hash = hash & 0xffffffff
	return '8%x' % hash

def pr( domain, session = None ):
	url = 'http://' \
		+ 'toolbarqueries.google.com' \
		+ '/tbr?client=navclient-auto&ch={hash}&features=Rank&q=info:{domain}'
	session = session or Session()
	url = url.format( hash=hash(domain), domain=domain )
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = session.request('get', url, headers=headers, timeout=10,
								allow_redirects=True, verify=False )
	rank = response.text.split(':')[-1].strip()
	return int( rank )
