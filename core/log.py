#!/usr/bin/env python

import logging

def log( level = logging.DEBUG, filename = None ):
	logging.basicConfig(filename=filename, level=level,
						format='[%(asctime)s %(levelname)s] %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S' )
	logging.getLogger().setLevel( level )
	requests_logger = logging.getLogger("requests")
	requests_logger.setLevel( logging.WARNING )
