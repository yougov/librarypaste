import abc

class DataStoreTest(object):
	@abc.abstractproperty
	def datastore(self):
		"""
		The datastore instance under test
		"""

	def test__store(self):
		uid = 'some-id'
		content = dict(baz='some-content')
		data = dict(foo='bar')
		res = self.datastore._store(uid, content, data)
		assert res is None
