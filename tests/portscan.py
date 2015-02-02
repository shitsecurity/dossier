#!/usr/bin/env python

import path

try:
	from recon.portscan import syn, tcp_ports, randomize
except ImportError:
	from recon.error import rage_quit
	rage_quit('scapy is NOT installed or NOT running as root')

print syn('google.com', ports=randomize(tcp_ports()))
