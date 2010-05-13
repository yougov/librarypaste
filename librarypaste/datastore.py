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



import uuid
from string import letters, digits
from random import choice

def shortkey():
    firstlast = list(letters + digits) 
    middle = firstlast + list('-_.')
    return ''.join((choice(firstlast), choice(middle), choice(middle), choice(middle), choice(firstlast)))
    
    
class DataStore(object):
    """Implements a datastore using an arbitrary backend. """
    def __init__(self, *args, **kwargs):
        pass
        
    def _store(self, uid, content):
        """Store the given dict of content at uid. Nothing returned."""
        raise NotImplementedError
        
    def _storeLog(self, nick, time, uid):
        """Adds the nick & uid to the log for a given time/order. No return."""
        raise NotImplementedError
    
    def _retrieve(self, uid):
        """Return a dict with the contents of the paste, including the raw
        data, if any, as the key 'data'. Must pass in uid, not shortid."""
        raise NotImplementedError
        
    def lookup(self, nick):
        """Looks for the most recent paste by a given nick.
        Returns the uid or None"""
        raise NotImplementedError
        
    def store(self, type, nick, time, fmt=None, code=None, filename=None, mime=None, data=None, makeshort=True):
        """Store code or a file. Returns a tuple containing the uid and shortid"""
        uid = str(uuid.uuid4())
        if makeshort:
            shortid = shortkey()
        else:
            shortid = None
            
        temp = {'uid' : uid, 'shortid' : shortid, 'type' : type, 'nick' : nick, 'time' : time,
            'fmt' : fmt, 'code' : code,
            'filename' : filename, 'mime' : mime, 'data' : data}
        paste = {}
        for k, v in temp.items():
            if v:
                paste[k] = v
        self._store(uid, paste)
        if nick:
            self._storeLog(nick, time, uid)
        return (uid, shortid)
    
    def retrieve(self, id):
        """Retrieve a paste. Returns a dictionary containing all metadata
        and the file data, if it's a file."""
        if len(id) < 10:
            shortid = id
            uid = self._lookupUid(shortid)
        else:
            uid = id
        return self._retrieve(uid)
        

class JsonDataStore(DataStore):
    """Stores using json encoded into files"""
    def __init__(self, repo):
        super(JsonDataStore, self).__init__()
        self.repo = repo
        if not os.path.exists(repo):
            os.mkdirs(repo)
        self.shortids = {}
    
    def _store(self, uid, content):
        data = content.pop('data')
        fd = open(os.path.join(self.repo, uid), 'wb')
        fd.write(json.dumps(content))
        fd.close()
        if data:
            fd = open(os.path.join(self.repo, '%s.raw' % uid), 'wb')
            fd.write(data)
            fd.close()
        if content['shortid']:
            self.shortids[content['shortid']] = uid
            open(os.path.join(self.repo, 'shortids.txt'), 'a').write('%s %s\n' % (content['shortid'], uid))
        
    def _storeLog(self, nick, time, uid):
        open(os.path.join(self.repo, 'log.txt'), 'a').write('%s %s\n' % (nick, uid))
    
    def lookup(self, nick):
        last = None
        for line in open(os.path.join(self.repo, 'log.txt')):
            who, uid = line.strip().rsplit(None, 1)
            if who == nick:
                last = uid
        return last
        
    def _lookupUid(self, shortid):
        if not self.shortids:
            for line in open(os.path.join(self.repo, 'shortids.txt')):
                l1, l2 = line.strip().rsplit(None, 1)
                self.shortids[l1] = l2
        try:
            uid = self.shortids[shortid]
        except KeyError:
            uid = None
        return uid

    def _retrieve(self, uid):
        paste = json.loads(open(os.path.join(self.repo, uid), 'rb').read())
        if paste['type'] == 'file':
            paste['data'] = open(os.path.join(self.repo, '%s.raw' % uid), 'rb').read()
        return paste