#!/usr/bin/env python

import path

from recon.ptr import ptr
from recon.utils import all_dns

import iptools

from recon.a import a
from recon.resolver import Resolver
from recon.host import reverse_dns, dnsdigger, yougetsignal, verify

from functools import partial

targets = iptools.IpRangeList(( '8.8.4.4', '8.8.4.4' ))

for target in targets:
    for domain in ptr( target ):
        print all_dns( domain )

print reverse_dns( 'google.com', engine=yougetsignal )

print filter(partial( verify, ips=a('google.com'), resolver=Resolver() ),
             reverse_dns( 'google.com', engine=dnsdigger ))
