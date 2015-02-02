#!/usr/bin/env python

from requests import Session
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

def fetch( url,
			session=None,
			method='get',
			data=None,
			headers={'User-Agent': 'Mozilla/5.0'},
			cookies={},
			timeout=10,
			encoding='utf-8' ):

	if not url.startswith('http'):
		url = 'http://{}'.format( url )
	session=session or Session()
	response = session.request( method, 
								url, 
								data=data,
								cookies=cookies,
								headers=headers,
								timeout=timeout,
								allow_redirects=True,
								verify=False )
	return response.text.encode('utf-8')
