import cherrypy
import time
import simplejson
import uuid
import cgi
import os
import time, datetime
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import get_formatter_by_name
from pygments import highlight
from mako.template import Template
from mako.lookup import TemplateLookup
import routes


lookup = TemplateLookup(directories=['templates'])

htmlformatter = get_formatter_by_name('html')


class PasteBinPage(object):

	def index(self):
		d = {}
		page = lookup.get_template('entry.html')

		d['title'] = "Library Paste"
		
		d['lexers'] = sorted([(l[0], l[1][0]) for l in get_all_lexers()])
		d['pre_nick'] = ('' if not 'paste-nick' in cherrypy.request.cookie 
		else cherrypy.request.cookie['paste-nick'].value)
		return page.render(**d)

	def post(self, fmt=None, nick=None, code=None, file=None):
		uid = str(uuid.uuid4())
		REPO = cherrypy.request.app.config['repo']['path']
		data = file.file.read()
		
		if data:
			filename = file.filename
			mime = file.type
			content = {'nick' : nick, 'time' : time.time(), 'type' : 'file',
				'mime' : mime, 'filename' : filename,}
			raw = open(os.path.join(REPO, '%s.raw' % uid), 'wb')
			raw.write(data)
			raw.close()
		else:
			content = {'nick' : nick, 'time' : time.time(), 'type' : 'code',
			'fmt' : fmt, 'code' : code}
		fd = open(os.path.join(REPO, uid), 'wb')
		fd.write(simplejson.dumps(content))
		fd.close()

		if nick:
			open(os.path.join(REPO, 'log.txt'), 'a').write('%s %s\n' % (nick, uid))
			cherrypy.response.cookie['paste-nick'] = nick
		
		raise cherrypy.HTTPRedirect(cherrypy.url(routes.url_for('viewpaste', pasteid=uid)))

class PasteViewPage(object):
	def index(self, pasteid=None):
		REPO = cherrypy.request.app.config['repo']['path']
		d = {}
		page = lookup.get_template('view.html')
		try:
			paste_data = simplejson.loads(open(os.path.join(REPO, pasteid), 'rb').read())
		except IOError:
			raise cherrypy.NotFound("The paste '%s' could not be found." % pasteid)
		if paste_data['type'] == 'file':
			raw = open(os.path.join(REPO, '%s.raw' % pasteid), 'rb').read()
			cherrypy.response.headers['Content-Type'] = paste_data['mime']
			cherrypy.response.headers['Content-Disposition'] = 'inline; filename="%s"' % paste_data['filename']
			cherrypy.response.headers['filename'] = paste_data['filename']
			return raw
			
		d['linenums'] = '\n'.join([str(x) for x in xrange(1, paste_data['code'].count('\n')+2)])
		if paste_data['fmt'] == '_':
			d['code'] = '<pre>%s</pre>' % cgi.escape(paste_data['code'])
		else:
			lexer = get_lexer_by_name(paste_data['fmt'])
			d['code'] = highlight(paste_data['code'], lexer, htmlformatter)
		d['pasteid'] = pasteid
		d['plainurl'] = cherrypy.url(routes.url_for(controller='plain', pasteid=pasteid))
		d['homeurl'] = cherrypy.url(routes.url_for(controller='paste', pasteid=None))
		d['title'] = 'Paste %s%s%s on %s' % (pasteid, 
			' (%s)' % paste_data['fmt'] if paste_data['fmt'] != '_' else '',
			' by %s' % paste_data['nick'] if paste_data['nick'] else '', 
		datetime.datetime.fromtimestamp(paste_data['time']).strftime('%b %d, %H:%M'))
		return page.render(**d)

class LastPage(object):
	def index(self, nick=''):
		REPO = cherrypy.request.app.config['repo']['path']
		last = ''
		for line in open(os.path.join(REPO, 'log.txt')):
			who, what = line.strip().rsplit(None, 1)
			if who == nick:
				last = what
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return last

class PastePlainPage(object):
	def index(self, pasteid=None):
		REPO = cherrypy.request.app.config['repo']['path']
		paste_data = simplejson.loads(open(os.path.join(REPO, pasteid), 'rb').read())
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return paste_data['code']
