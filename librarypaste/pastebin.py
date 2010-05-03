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
from Cheetah.Template import Template

htmlformatter = get_formatter_by_name('html')


class PasteBinPage(object):
	title = "YouGov Pastebin"

	template = Template(file='templates/base.tmpl')
	body = Template(file='templates/entry.tmpl')

	def index(self):
		page = Template(file='templates/entry.tmpl')
		page.title = "Pastebin"
		
		page.lexers = sorted([(l[0], l[1][0]) for l in get_all_lexers()])
		page.pre_nick = ('' if not 'paste-nick' in cherrypy.request.cookie 
		else cherrypy.request.cookie['paste-nick'].value)
		return page

	def onFormSuccess_paste(self, page, fmt=None, nick=None, code=None):
		uid = str(uuid.uuid4())

		fd = open(os.path.join(REPO, uid), 'wb')
		fd.write(simplejson.dumps({'fmt':fmt, 'nick':nick, 'code':code, 'time' : time.time()}))
		fd.close()

		if nick:
			open(os.path.join(REPO, 'log.txt'), 'a').write('%s %s\n' % (nick, uid))
			cherrypy.response.cookie['paste-nick'] = nick
		
		raise cherrypy.HTTPRedirect(pasteid=uid)

class PasteViewPage(object):
	template = Template(file='templates/base.tmpl')
	body = Template(file='templates/view.tmpl')

	def index(self, page, pasteid=None):
		paste_data = simplejson.loads(open(os.path.join(REPO, pasteid), 'rb').read())
		page.linenums = '\n'.join([str(x) for x in xrange(1, paste_data['code'].count('\n')+2)])
		if paste_data['fmt'] == '_':
			page.code = '<pre>%s</pre>' % cgi.escape(paste_data['code'])
		else:
			lexer = get_lexer_by_name(paste_data['fmt'])
			page.code = highlight(paste_data['code'], lexer, htmlformatter)
		page.pasteid = pasteid
		page.title = 'Paste %s%s%s on %s' % (pasteid, 
		' (%s)' % paste_data['fmt'] if paste_data['fmt'] != '_' else '',
		' by %s' % paste_data['nick'] if paste_data['nick'] else '', 
		datetime.datetime.fromtimestamp(paste_data['time']).strftime('%b %d, %H:%M'))

class LastPage(object):
	def index(self, page, nick=''):
		last = ''
		for line in open(os.path.join(REPO, 'log.txt')):
			who, what = line.strip().rsplit(None, 1)
			if who == nick:
				last = what
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return last

class PastePlainPage(object):
	def index(self, page, pasteid=None):
		paste_data = simplejson.loads(open(os.path.join(REPO, pasteid), 'rb').read())
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return paste_data['code']
