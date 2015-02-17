#!/usr/bin/env python

from recon.a import aaaa, a
from recon.soa import soa
from recon.ns import ns
from recon.cname import cname
from recon.mx import mx
from recon.srv import srv

from itertools import chain

def any( domain, resolver=None ):
	return reduce( lambda x,y: x+y,
					filter( lambda _: len(_)>0,
							map(lambda _: _(domain, resolver=resolver ),
								[ a, aaaa, soa, ns, cname, mx, srv ] )),
					[])
