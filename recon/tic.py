#!/usr/bin/env python

import http

from lxml import etree

def tic( domain, session=None ):
    url = 'http://' \
        + 'bar-navig.yandex.ru' \
        + '/u?ver=2&lang=1049&url=http://{}&show=1&thc=0'
    url = url.format( domain )
    data = http.fetch( url, session=session )
    root = etree.XML( data, parser=etree.HTMLParser(encoding="utf-8") )
    rank = root.xpath('//tcy[@value]')[0].get('value')
    return int( rank )
