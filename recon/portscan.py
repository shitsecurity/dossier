#!/usr/bin/env python

import yaml
import os.path

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

from itertools import chain
from random import shuffle
from copy import copy

def localhost( host ):
	if host.startswith('127.'):
		msg = 'scanning localhost is NOT reliable, consult scapy docs'
		logging.warning(msg)
		conf.L3socket=L3RawSocket # scapy localhost magic

def syn( host, ports, interval=0.5, retry=2, timeout=2 ):
	localhost( host )
	packet = IP( dst=host )/TCP(sport=RandShort(), dport=ports, flags="S")
	results, ignored = sr( packet,  inter=interval,
									timeout=timeout,
									retry=retry,
									verbose=False )
	return [ _[0].dport for _ in
			results.filter( lambda ( s, r ): TCP in r and r[TCP].flags&2 ) ]

def udp( host, ports, interval=0.5, retry=2, timeout=2 ):
	localhost( host )
	packet = IP( dst=host )/UDP(sport=RandShort(),dport=ports)
	results, ignored = sr( packet,  inter=interval,
									timeout=timeout,
									retry=retry,
									verbose=False )
	return [ _[0].dport for _ in results.filter( lambda ( s, r ): UDP in r ) ]

class Port( yaml.YAMLObject ):
	yaml_tag = '!Port'

	def __repr__( self ):
		return '<{cls} {port}>'.format( cls=self.__class__.__name__,
										port=self.port )

	def prepare( self ):
		return [self.port]

class PortRange( yaml.YAMLObject ):
	yaml_tag = '!PortRange'

	def __repr__( self ):
		return '<{cls} {start}-{end}>'. format( cls=self.__class__.__name__,
												start=self.start,
												end=self.end )

	def prepare( self ):
		return [ _ for _ in xrange(self.start,self.end)]

def tcp_ports( *args, **kwargs ):
	return load_ports( 'tcp', *args, **kwargs )

def udp_ports( *args, **kwargs ):
	return load_ports( 'udp', *args, **kwargs )

def load_ports( type, file='ports.yaml' ):
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
						'..',
						'data',
						file )
	with open(path,'rb') as fh:
		return map( int,
					reduce( lambda ctx,ii: ctx+ii.prepare(),
							yaml.load( fh )[type],
							[] ))

def randomize( ports ):
	random_ports = copy(ports)
	shuffle( random_ports )
	return random_ports
