#!/usr/bin/env python

import urllib2
import argparse
import time
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('port', type=int)
args = parser.parse_args()

root = 'http://{host}:{port}/'.format(**vars(args))
for try_ in itertools.count(1):
	try:
		urllib2.urlopen(root)
		break
	except urllib2.URLError as exc:
		if 'refused' not in str(exc).lower() or try_ >= 3:
			raise
		time.sleep(3)
