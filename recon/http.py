#!/usr/bin/env python

import requests.packages
requests.packages.urllib3.disable_warnings()

from requests import Session as RequestsSession
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

class Session( RequestsSession ):

	def __init__( self, *args, **kwargs ):
		super( Session, self ).__init__( *args, **kwargs )
		self.headers['User-Agent'] = 'Mozilla/5.0'

def fetch( url,
			session=None,
			method='get',
			data=None,
			headers={},
			cookies={},
			timeout=10,
			encoding='utf-8' ):

	if not url.startswith('http'):
		url = 'http://{}'.format( url )
	if session is None:
		session = Session()
	response = session.request( method,
								url,
								data=data,
								cookies=cookies,
								headers=headers,
								timeout=timeout,
								allow_redirects=True,
								verify=False )
	return response.text.encode(encoding)
