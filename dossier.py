#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import print_function

import sys
import argparse

from ctl import actors, run, wait, configure, config
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
    parser.add_argument('--conf', metavar='', dest='config', type=str,
                        help='config file', default='config.conf' )
    parser.add_argument('--file', metavar='', dest='file', type=str,
                        help='write report to file', default=None )
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

    light = [
        'report',
        'verbose',
        'ip.reverse',
        'ns.ext',
        'ns.lookup',
        'ns.google',
        'ip.geo',
    ]

    if args.light and args.all:
        parser.error("go home hacker, you're drunk")

    if args.enabled and args.all:
        parser.error('shit happens bro')

    if args.light:
        args.enabled += light

    args.enabled = list(set(args.enabled))

    names = [ _.name for _ in actors() ]

    for name in args.enabled + args.disabled:
        if name not in names:
            parser.error('invalid plugin {}'.format( name ))

    if args.list:
        [ print(' [*] {}'.format( _ )) for _ in names ]
        sys.exit()

    if not any([ args.ip, args.range, args.domain ]):
        parser.error('select target')

    return args

if __name__ == "__main__":
    args = parse_args()

    channels, plugins = run(include=args.enabled,
                            exclude=args.disabled,
                            all=args.all)
    configure( config( args.config ), plugins )

    if args.file and plugins.loaded('report'):
        plugins.get('report').set_option('file',args.file)

    plugins.invoke()

    if args.ip or args.range:
        for ip in IpRangeList(*( args.ip+args.range )):
            channels.publish( 'ip.*', ip )

    if args.domain:
        for domain in args.domain:
            channels.publish( 'domain.*', domain )

    wait()
    plugins.shutdown()
