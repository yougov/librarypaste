#!/usr/bin/env python

import urllib2
import argparse

import portend

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('port', type=int)
args = parser.parse_args()

portend.occupied(args.host, args.port, timeout=3)
root = 'http://{host}:{port}/'.format(**vars(args))
urllib2.urlopen(root)
