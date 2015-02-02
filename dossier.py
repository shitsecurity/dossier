#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import print_function

import sys
import argparse

from ctl import actors, run, wait
from iptools import IpRangeList

NORMAL = '\033[m'; DARK_GREEN = '\033[32m'

print('''{green}


             ██████╗  ██████╗ ███████╗███████╗██╗███████╗██████╗ 
             ██╔══██╗██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔══██╗
             ██║  ██║██║   ██║███████╗███████╗██║█████╗  ██████╔╝
             ██║  ██║██║   ██║╚════██║╚════██║██║██╔══╝  ██╔══██╗
             ██████╔╝╚██████╔╝███████║███████║██║███████╗██║  ██║
             ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝
                               @shitsecurity
{normal}
'''.format( green=DARK_GREEN, normal=NORMAL ))

def parse_args():
	parser = argparse.ArgumentParser(description='find some shit')
	parser.add_argument('--light', action='store_true', dest='light',
						help='enable light modules' )
	parser.add_argument('--all', action='store_true', dest='all',
						help='enable all modules' )
	parser.add_argument('--file', metavar='', dest='file', type=str,
						help='write results to file', default=None )
	parser.add_argument('--disable', metavar='', dest='disabled', type=str,
						help='disable modules', nargs='+', default=[] )
	parser.add_argument('--enable', metavar='', dest='enabled', type=str,
						help='enable modules', nargs='+', default=[] )
	parser.add_argument('--list', action='store_true', dest='list',
						help='list modules' )
	parser.add_argument('--ip', metavar='', dest='ip', type=str,
						help='ip addresses', nargs='+', default=[] )
	parser.add_argument('--ip-range', metavar='', dest='range', type=str,
						help='ip ranges', nargs='+', default=[] )
	parser.add_argument('--domain', metavar='', dest='domain', type=str,
						help='domain names', nargs='+', default=[] )
	args = parser.parse_args()

	heavy = [
			'subdomains.brute',
			'domain.reverse',
			'scan.syn',
			'rank.tic',
			'rank.pr',
			'ip.subnet',
	]

	light = [
			'file',
			'log',
			'ip.reverse',
			'domain.meta',
			'domain.lookup',
			'domain.google',
			'ip.bing',
	]

	if args.light and args.all:
		parser.error("go home hacker, you're drunk")

	if args.light:
		args.enabled += light

	if args.all:
		args.enabled = light+heavy

	args.enabled = list(set(args.enabled))

	if args.enabled and args.disabled:
		parser.error('u dun goofd')

	if not any([ args.ip, args.range, args.domain, args.list ]):
		parser.error('select target')

	return args

if __name__ == "__main__":
	args = parse_args()

	if args.list:
		[ print(' [*] {}'.format(_.name)) for _ in actors() ]
		sys.exit()

	channels, threads = run( include=args.enabled, exclude=args.disabled )

	if args.file:
		channels.publish( 'opt.file', args.file )

	if args.range:
		for ip in IpRangeList(*( args.ip+args.range )):
			channels.publish( 'ip.*', ip )

	if args.domain:
		for domain in args.domain:
			channels.publish( 'domain.*', domain )

	wait()
	channels.publish( 'signal', 'shutdown' )
	wait()
