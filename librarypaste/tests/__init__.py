import abc
import datetime

import pkg_resources

class DataStoreTest(object):
	common_content = dict(
		nick = 'nick',
		time = datetime.datetime.now(),
		makeshort = True,
	)
	code_content = common_content.copy()
	file_content = common_content.copy()
	code_content.update(
		type='code',
		fmt = 'python',
		code = pkg_resources.resource_string('librarypaste', 'pastebin.py'),
	)
	file_content.update(
		type = 'file',
		mime = 'image/png',
		filename = 'librarypaste.png',
		data = pkg_resources.resource_string('librarypaste',
			'static/librarypaste.png')
	)
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
