# Summary

Actor-based network recon tool with a publisher-subscriber feedback loop model.

# Modules

```
ns.brute   - brute dns subdomains
ns.whois   - whois by domain
ip.whois   - whois by ip
ip.geo     - geoip
verbose    - log to stdout
report     - log to file
scan.syn   - tcp syn scan ip
scan.udp   - udp connect scan ip
rank.pr    - page rank by domain
rank.tic   - thematic citation index (tic) by domain
ns.lookup  - domain name to ip (a, aaaa)
ns.ext     - domain name to ip (soa, ns, mx, srv, cname)
ns.reverse - neighboring domains by domain via third party api
ip.reverse - ptr record by ip
ip.bing    - domains via bing by ip
ns.google  - subdomains via google by domain
ip.subnet  - ip via relevant ptr from subnet
```

# Installation

lxml deps:

```
sudo apt-get install libxml2-dev libxslt-dev
```

python modules:

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

scapy (optional):

```
cd install
bash scapy.sh
python scapy/setup.py install
```

# Usage

Specify multiple targets in multiple formats:

```
./dossier.py --ip 192.168.0.1 192.168.0.2 --ip-range 192.168.1.0/24 192.168.2.0/28 --domain localhost local
```

Brute subdomains and check google:

```
./dossier.py --enable verbose ns.brute ns.google --domain [domain]
```

Find neighboring domains via bing:

```
./dossier.py --enable verbose ip.bing ns.lookup --domain [domain]
```

Find neighboring domains via third party api and fetch their pr and tic:

```
./dossier.py --enable verbose ns.reverse rank.pr rank.tic --domain [domain]
```

Portscan, geoip, whois all hosts in each /24 (non-overlapping) of all subdomains and log to file:

```
./dossier.py --enable verbose report ns.lookup ns.brute ip.subnet scan.syn ip.whois ip.geo --domain [domain] --file results.txt
```

# Scapy

enable scapy:

```
sudo bash
. env/bin/activate
```
