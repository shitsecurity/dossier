#!/usr/bin/env python

import path

import iptools

from recon.ptr import ptr, verify
from recon.subnet import subnet
from recon.resolver import Resolver
from recon.utils import all_dns

from functools import partial

in_subnet = partial( subnet, ['google.com',] )

targets = iptools.IpRangeList(( '127.0.0.1', '127.0.0.255' ))

resolver = Resolver()
names = []

for target in targets:
    for domain in ptr( target, resolver=resolver ):
        if verify( target, domain, resolver=resolver ):
            names += filter( in_subnet, all_dns( domain ))

print names
