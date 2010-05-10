#!/usr/bin/env python
# encoding: utf-8
"""
datastore.py

Created by Chris Mulligan on 2010-05-09.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import os

try:
    import simplejson as json
except ImportError:
    import json

try:
    from google.appengine.ext import db
except ImportError:
    pass
    

class DataStore(object):
    """Non-backend specific datastore. Can use json or google app engine, or potentially others."""
    def __init__(self, type, repopath=None):
        """Pass in a type ('gae' or 'json'), and if json a path to the repository."""
        super(DataStore, self).__init__()
        self.type = type
        self.repopath = repopath
        
try:
    import simplejson as json
except ImportError:
    import json
    
class JsonDataStore(DataStore):
    """Implements a datastore using flat json files in a directory."""
    def __init__(self, repopath):
        self.repopath = repopath
        if not os.path.exist(self.repopath):
            os.mkdir(self.repopath)
    
    def store(self, **kwargs):
        """docstring for storeCode"""
        for k in ['type', 'nick', 'time']:
            if k not in kwargs:
                raise 
        if kwargs['type']