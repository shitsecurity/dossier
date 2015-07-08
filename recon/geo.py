#!/usr/bin/env python

from geoip import geolite2

from exceptions import safe

@safe( AttributeError )
def geoip_country( ip ):
    return geolite2.lookup( ip ).country
