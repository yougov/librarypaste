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
    try:
        import json
    except ImportError:
        pass

try:
    from google.appengine.ext import db
except ImportError:
    pass

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
        
    def _storeCode(self, uid, content):
        """Store the given dict of content at uid. Nothing returned."""
        raise NotImplementedError
        
    def _storeFile(self, uid, content, data):
        """Store the given data & content dictionary. Nothing returned."""
        raise NotImplementedError
        
    def _storeLog(self, nick, time, uid):
        """Adds the nick & uid to the log for a given time/order. No return."""
        raise NotImplementedError
    
    def _retrieve(self, uid):
        """Return a dict with the contents of the paste, including the raw
        data, if any, as the key 'data'. Must pass in uid, not shortid."""
        raise NotImplementedError
        
    def lookupLog(self, nick):
        """Looks for the most recent paste by a given nick.
        Returns the uid or None"""
        raise NotImplementedError
        
    def storeCode(self, nick, time, fmt, code, makeshort=True):
        """Store a piece of code. Returns a tuple containing the uid and shortid"""
        uid = str(uuid.uuid4())
        if makeshort:
            shortid = shortkey()
        else:
            shortid = None
        paste = {'uid' : uid, 'shortid' : shortid, 'type' : 'code', 'nick' : nick,
            'time' : time, 'fmt' = fmt, 'code' : code}
        self._storeCode(uid, paste)
        if nick:
            self._storeLog(nick, time, uid)
        return (uid, shortid)
    
    def storeFile(self, nick, time, filename, mime, data, makeshort=True):
        """Store a file, returns a tuple containing the uid and shortid."""
        uid = str(uuid.uuid4())
        if makeshort:
            shortid = shortkey()
        else:
            shortid = None
        paste = {'uid' : uid, 'shortid' : shortid, 'type' = 'file', 'nick' : nick,
            'time' : time, 'filename' : filename, 'mime' : mime}
        self._storeFile(uid, paste, data)
        return (uid, shortid)
    
    def retrieve(self, id):
        """Retrieve a paste. Returns a dictionary containing all metadata
        and the file data, if it's a file."""
        if len(id) < 10:
            shortid = id
            uid = self._lookupLog(shortid)
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
    
    def _storeCode(self, uid, content):
        fd = open(os.path.join(self.repo, uid), 'wb')
        fd.write(json.dumps(content))
        fd.close()
        if content['shortid']:
            self.shortids[content['shortid']] = uid
            open(os.path.join(self.repo, 'shortids.txt'), 'a').write('%s %s\n' % (content['shortid'], uid))
        
    def _storeFile(self, uid, content, data):
        raw = open(os.path.join(self.repo, '%s.raw' % uid), 'wb')
        raw.write(data)
        raw.close()
        fd = open(os.path.join(self.repo, uid), 'wb')
        fd.write(json.dumps(content))
        fd.close()
        if content['shortid']:
            self.shortids[content['shortid']] = uid
            open(os.path.join(self.repo, 'shortids.txt'), 'a').write('%s %s\n' % (content['shortid'], uid))
    
    def _storeLog(self, nick, time, uid):
        open(os.path.join(self.repo, 'log.txt'), 'a').write('%s %s\n' % (nick, uid))
    
    def lookupLog(self, nick):
        last = None
        for line in open(os.path.join(self.repo, 'log.txt')):
            who, uid = line.strip().rsplit(None, 1)
            if who == nick:
                last = uid
        return last

    def _retrieve(self, uid):
        paste = json.loads(open(os.path.join(self.repo, uid), 'rb').read())
        if paste_data['type'] == 'file':
            paste['data'] = open(os.path.join(self.repo, '%s.raw' % uid), 'rb').read()
        return paste