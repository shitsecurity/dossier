#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

def emoji():
    return random.choice( [ '٩(×̯×)۶',
                            '✖_✖',
                            '(┛◉Д◉)┛┻━┻',
                            '(╯°□°）╯︵ ┻━┻',
                            '\_(͡๏̯͡๏)_/',
                            'o(≧o≦)o',
                            '╭∩╮(-_-)╭∩╮',
                            'ᕙ(⇀‸↼‶)ᕗ' ] )

def vent_rage( msg, status ):
    print '[!] {}'.format( msg )
    print ''
    print '{} {}'.format(status,emoji())
    print ''

def rage_quit( msg ):
    print '[!] {}'.format( msg )
    print ''
    print 'Terminating.. {}'.format(emoji())
    print ''
    sys.exit(1)

def dummy_none( *args, **kwargs ): pass

def dummy_iter( *args, **kwargs ): return []
