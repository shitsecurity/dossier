#!/usr/bin/env python

import http

def hash( domain ):
    seed = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE."\
           "Yes, I'm talking to you, scammer."
    hash = 0x01020345
    for i in range( len( domain )):
        hash = hash ^ ord( seed[ i % len( seed ) ]) ^ ord( domain[ i ] )
        hash = hash >> 23 | hash << 9
        hash = hash & 0xffffffff
    return '8%x' % hash

def pr( domain, session=None ):
    url = 'http://' \
        + 'toolbarqueries.google.com' \
        + '/tbr?client=navclient-auto&ch={hash}&features=Rank&q=info:{domain}'
    url = url.format( hash=hash(domain), domain=domain )
    data = http.fetch( url, session=session )
    rank = data.split(':')[-1].strip()
    if rank == '':
        rank = 0
    else:
        rank = int(rank)
    return rank
