#!/usr/bin/env python

from core import concurrency
from core.actor import Actor, Channels, wait, Plugins
from core.thread import spawn

from straight.plugin import load
from configparser import ConfigParser

def actors():
    return [ _ for _ in load( 'actors', subclasses=Actor ) ]

def configure( config, plugins ):
    for name, plugin in plugins.items():
        if config.has_section( name ):
            plugin.configure( config )

def config( file ):
    config_parser = ConfigParser()
    with open( file, 'rb' ) as fh:
        config_parser.readfp( fh )
    return config_parser

def run( include =[], exclude=[], all=False ):
    channels = Channels()
    def accept( plugin ):
        if all or include and plugin.name in include:
            if not exclude or plugin.name not in exclude:
                return True
    greenlets = spawn( filter(accept, actors()), channels )
    return (channels,Plugins(greenlets))

if __name__ == "__main__":
    light = [
        'report',
        'verbose',
        'ip.reverse',
        'ns.ext',
        'ns.lookup',
        'ns.google',
        'ip.bing',
        'ip.geo',
    ]
    channels, plugins = run( include=light )
    configure(config('config.conf'),plugins)
    plugins.get('report').set_option('file','results.txt')
    plugins.invoke()
    #channels.publish( 'domain.*', 'google.com' )
    #channels.publish( 'ip.*', '8.8.8.8' )
    #channels.publish( 'domain.*', 'yandex.ru' )
    wait()
    plugins.shutdown()
