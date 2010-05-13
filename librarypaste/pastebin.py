# encoding: utf-8
import cherrypy
import time
from cgi import escape
import os
import datetime
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments import highlight
from mako.template import Template
from mako.lookup import TemplateLookup
import routes

BASE = os.path.abspath(os.path.dirname(__file__))

lookup = TemplateLookup(directories=[os.path.join(BASE, 'templates')])


class PasteBinPage(object):

    def index(self):
        d = {}
        page = lookup.get_template('entry.html')

        d['title'] = "Library Paste"
        
        d['lexers'] = sorted([(l[0], l[1][0]) for l in get_all_lexers()])
        d['pre_nick'] = ('' if not 'paste-nick' in cherrypy.request.cookie 
            else cherrypy.request.cookie['paste-nick'].value)
        try:
            d['short'] = bool(int(cherrypy.request.cookie['paste-short'].value))
        except KeyError:
            d['short'] = True
        return page.render(**d)

    def post(self, fmt=None, nick=None, code=None, file=None, makeshort=None):
        ds = cherrypy.request.app.config['datastore']['datastore']
        data = file.file.read()
        content = {'nick' : nick, 'time' : datetime.datetime.now(), 'makeshort' : bool(makeshort)}
        if data:
            filename = file.filename
            mime = file.type
            content.update({'type' : 'file', 'mime' : mime, 'filename' : filename, 'data' : data})
        else:
            content.update({'type' : 'code', 'fmt' : fmt, 'code' : code})
        (uid, shortid) = ds.store(**content)

        if nick:
            cherrypy.response.cookie['paste-nick'] = nick
            cherrypy.response.cookie['paste-nick']['expires'] = 60 * 60 * 24 * 30 #store cookies for 30 days
        
        if makeshort:
            redirid = shortid
            cherrypy.response.cookie['paste-short'] = 1
            cherrypy.response.cookie['paste-short']['expires'] = 60 * 60 * 24 * 30 #store cookies for 30 days
        else:
            redirid = uid
            cherrypy.response.cookie['paste-short'] = 0
            cherrypy.response.cookie['paste-short']['expires'] = 60 * 60 * 24 * 30 #store cookies for 30 days
        raise cherrypy.HTTPRedirect(cherrypy.url(routes.url_for('viewpaste', pasteid=redirid)))

class PasteViewPage(object):
    def index(self, pasteid=None):
        ds = cherrypy.request.app.config['datastore']['datastore']
        d = {}
        page = lookup.get_template('view.html')
        try:
            paste_data = ds.retrieve(pasteid)
        except:
            raise cherrypy.NotFound("The paste '%s' could not be found." % pasteid)
        if paste_data['type'] == 'file':
            cherrypy.response.headers['Content-Type'] = paste_data['mime']
            cherrypy.response.headers['Content-Disposition'] = 'inline; filename="%s"' % paste_data['filename']
            cherrypy.response.headers['filename'] = paste_data['filename']
            return paste_data['data']
            
        d['linenums'] = '\n'.join([str(x) for x in xrange(1, paste_data['code'].count('\n')+2)])
        if paste_data['fmt'] == '_':
            lexer = get_lexer_by_name('text')
        else:
            lexer = get_lexer_by_name(paste_data['fmt'])
        htmlformatter = HtmlFormatter(linenos='table')
        d['code'] = highlight(paste_data['code'], lexer, htmlformatter)
        d['pasteid'] = pasteid
        d['plainurl'] = cherrypy.url(routes.url_for(controller='plain', pasteid=pasteid))
        d['homeurl'] = cherrypy.url(routes.url_for(controller='paste', pasteid=None))
        d['title'] = 'Paste %s%s%s on %s' % (pasteid, 
            ' (%s)' % paste_data['fmt'] if paste_data['fmt'] != '_' else '',
            ' by %s' % paste_data['nick'] if paste_data['nick'] else '', 
        paste_data['time'].strftime('%b %d, %H:%M'))
        return page.render(**d)

class LastPage(object):
    def index(self, nick=''):
        ds = cherrypy.request.app.config['datastore']['datastore']
        last = ds.lookup(nick)
        if last:
            raise cherrypy.HTTPRedirect(cherrypy.url(routes.url_for('viewpaste', pasteid=last)))
        else:
            raise cherrypy.NotFound(nick)

class PastePlainPage(object):
    def index(self, pasteid=None):
        ds = cherrypy.request.app.config['datastore']['datastore']
        paste_data = ds.retrieve(pasteid)
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return paste_data['code']

        
class AboutPage(object):
    def index(self):
        d = {}
        page = lookup.get_template('about.html')
        d['title'] = 'About Library Paste'
        d['about'] = '''
        <p>Library Paste is an open source library paste engine - you're using an example of it right now! It was originally created by Jamie Turner, and modified and open sourced by Chris Mulligan. Right now the closest thing to a home page is its BitBucket account: <a href="http://bitbucket.org/chmullig/librarypaste">http://bitbucket.org/chmullig/librarypaste</a></p>
        <p>Using Library Paste is really simple - it can do just a couple things. You can upload text/code/files, and you can view them. Each paste is identified by a UUID; or optionally by a 5 character short code. Just copy the URL you have and share it with whomever you want. You can view pastes simply by appending the paste ID (either one) to the main URL.</p>
        <p>Library Paste can also take files and share them. It will attempt to serve back the files with whatever MIME type they were uploaded with - so if you attach a picture it will come through as a picture. Although it has a long URL, if you try to download the file or save it the original URL will come through. Right now there are no explicit limits on file size, however the web server and/or client may enforce some.</p>
        <p>One "hidden" feature is that you can find the last paste by a given nickname. You simple to go the url last/$username and you'll get redirected to their most recent paste, or given a 404 if it's not found. This is useful for IRC bots, for example.</p>
        <p>If you'd like your own, Library Paste is easy to setup. It's written in python using cherrypy, you can download the code at the bitbucket account listed above. If you have any feedback, questions or comments please send them along, via bitbucket, <a href="http://twitter.com/chmullig" alt="@chmullig on twitter">@chmullig</a> or chmullig@gmail.com.</p>
        '''
        return page.render(**d)