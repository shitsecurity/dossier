#!/usr/bin/env python

try:

	from recon.portscan import syn as syn_scan, udp as udp_scan
	from recon.portscan import tcp_ports, udp_ports, randomize

	def syn( host, ports=None, *args, **kwargs ):
		return syn_scan(host,
						randomize(ports or tcp_ports()),
						*args,
						**kwargs)

	def udp( host, ports=None, *args, **kwargs ):
		return udp_scan(host,
						randomize(ports or udp_ports()),
						*args,
						**kwargs)

except ImportError:

	from recon.error import vent_rage, dummy_iter as syn, dummy_iter as udp

	vent_rage ( 'scapy is NOT installed or NOT running as root',
				'Disabling support for raw sockets..' )
