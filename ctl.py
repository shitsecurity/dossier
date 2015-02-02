#!/usr/bin/env python

from core import concurrency
from core.actor import Actor, Channels, wait, Queue
from core.thread import spawn, start

from straight.plugin import load

def actors():
	return [ x for x in load( 'actors', subclasses=Actor ) ]

def run( include =[], exclude=[] ):
	channels = Channels()
	greenlets = start(spawn(filter( lambda _ : exclude and _.name not in exclude
											or include and _.name in include,
									actors() ),
							channels ))
	return (channels,greenlets)

if __name__ == "__main__":
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
	channels, threads = run( include=light )
	channels.publish( 'opt.file', 'results.txt' )
	channels.publish( 'domain.*', 'google.com' )
	#channels.publish( 'ip.*', '8.8.8.8' )
	#channels.publish( 'domain.*', 'yandex.ru' )
	wait()
	channels.publish( 'signal', 'shutdown' )
	wait()
