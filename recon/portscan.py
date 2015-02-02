#!/usr/bin/env python

import yaml
import os.path

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

from itertools import chain
from random import shuffle
from copy import copy

def syn( host, ports, timeout=5 ):
	packet = IP( dst=host )/TCP(sport=RandShort(),
								dport=ports,
								flags="S")
	results, ignored = sr( packet, timeout=5, verbose=False )
	open=[]
	for result in results:
		for sa in result[1::2]:
			if sa[1].flags==0x12:
				open.append( sa.sport )
	return open

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
		return [ x for x in xrange(self.start,self.end)]

def tcp_ports( file='ports.yaml' ):
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
						'..',
						'data',
						file )
	with open(path,'rb') as fh:
		return map( int,
					reduce( lambda ctx,ii: ctx+ii.prepare(),
							yaml.load( fh )['tcp'],
							[] ))

def randomize( ports ):
	random_ports = copy(ports)
	shuffle( random_ports )
	return random_ports
