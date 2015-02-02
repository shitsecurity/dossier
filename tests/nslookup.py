#!/usr/bin/env python

import path

from recon.a import aaaa, a
from recon.soa import soa
from recon.ns import ns
from recon.cname import cname
from recon.mx import mx
from recon.srv import srv

from recon.any import any

print a( 'www.google.com' )
print aaaa( 'www.google.com' )
print cname( 'www.google.com' )
print mx( 'gmail.com' )
print srv( 'jabber.org' )
print ns('google.com')
print soa('google.com')
print any('google.com')
