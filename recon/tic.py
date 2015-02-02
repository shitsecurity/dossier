#!/usr/bin/env python

from lxml import etree
from requests import Session
from requests.exceptions import Timeout

def tic( domain, session = None ):
	url = 'http://' \
		+ 'bar-navig.yandex.ru' \
		+ '/u?ver=2&lang=1049&url=http://{}&show=1&thc=0'
	session = session or Session()
	url = url.format( domain )
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = session.request('get', url, headers=headers, timeout=10,
								allow_redirects=True, verify=False )
	root = etree.XML(response.text.encode('utf8'))
	rank = root.xpath('//tcy[@value]')[0].get('value')
	return int( rank )
