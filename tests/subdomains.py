#!/usr/bin/env python

import path

from recon.subdomain import brute, subdomains, Subdomain

print subdomains('../data/subdomains.wl')

print brute('www.google.com')
print brute('doesnotexist.google.com')

ya=Subdomain('ya.ru')
print ya.brute('www')
print ya.brute('yayaya')
