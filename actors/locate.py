#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from geo import geoip_country

class GeoIPActor( Actor ):

    name = 'ip.geo'

    listeners =  [
        'ip.geo',
        'ip.*',
    ]

    @forever
    @action
    @unique
    def act( self, ip ):
        country = geoip_country( ip )
        self.channels.publish('geoip.*', { 'ip': ip, 'country': country })
