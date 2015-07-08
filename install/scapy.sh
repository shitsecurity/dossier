#!/bin/bash

sudo apt-get install mercurial tcpdump
hg clone http://bb.secdev.org/scapy
cd scapy
python setup.py install
