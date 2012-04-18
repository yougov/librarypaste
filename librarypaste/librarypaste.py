#!/usr/bin/env python
# encoding: utf-8

import os

import cherrypy

import jsonstore
from pastebin import (BASE, PasteBinPage, PasteViewPage, LastPage,
    PastePlainPage, FilePage, AboutPage)

def main():
    mapper = cherrypy.dispatch.RoutesDispatcher()
    mapper.connect('paste', '', PasteBinPage(),
        action='post', conditions=dict(method=['POST']))
    mapper.connect('paste', '', PasteBinPage())
    mapper.connect('about', 'about', AboutPage())
    mapper.connect('plain', 'plain/:pasteid', PastePlainPage())
    mapper.connect('last', 'last/:nick', LastPage())
    mapper.connect('file', 'file/:pasteid', FilePage())
    mapper.connect('viewpaste', ':pasteid', PasteViewPage())

    repo = os.path.join(os.getcwd(), 'repo')
    ds = jsonstore.JsonDataStore(repo)
    # Cherrypy configuration here
    app_conf = {
        'global': {
            'server.socket_host': '::0',
        },
        '/': {'request.dispatch': mapper},
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(BASE, 'static'),
        },
        'repo': {'path': repo},
        'datastore': {'datastore': ds, 'type': 'json'},
        'lexers': {'favorites': ['python']},
        'branding': {
            'name': 'Library',
            'logo source': '/static/librarypaste.png',
        }
    }

    cherrypy.tree.mount(root=None, config=app_conf)
    cherrypy.quickstart(None, '', config=app_conf)

if __name__ == '__main__':
    '''
    Useful for development mode
    '''
    main()
