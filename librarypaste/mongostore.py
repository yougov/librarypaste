import pymongo
import bson

from datastore import DataStore

class MongoDBDataStore(pymongo.Connection, DataStore):
    db_name = 'librarypaste'

    @property
    def db(self):
        return self[self.db_name]

    def _store(self, uid, content, data=None):
        """Store the given dict of content at uid. Nothing returned."""
        doc = dict(uid=uid)
        if data:
            doc.update(data=bson.Binary(data))
        doc.update(content)
        self.db.pastes.save(doc)

    def _storeLog(self, nick, time, uid):
        """Adds the nick & uid to the log for a given time/order. No return."""
        query = dict(uid=uid)
        update = {'$set': dict(nick=nick, time=time)}
        self.db.pastes.update(query, update)

    def _retrieve(self, uid):
        """Return a dict with the contents of the paste, including the raw
        data, if any, as the key 'data'. Must pass in uid, not shortid."""
        query = dict(uid=uid)
        return self.db.pastes.find_one(query)

    def lookup(self, nick):
        """Looks for the most recent paste by a given nick.
        Returns the uid or None"""
        query = dict(nick=nick)
        order = dict(time=pymongo.DESCENDING)
        recs = self.db.pastes.find(query).order(order).limit(1)
        try:
            return next(recs)['uid']
        except StopIteration:
            pass

    def _lookupUid(self, shortid):
        query = dict(shortid=shortid)
        rec = self.db.pastes.find_one(query)
        return rec['uid']
