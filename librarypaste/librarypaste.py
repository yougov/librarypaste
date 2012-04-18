#!/usr/bin/env python
# encoding: utf-8

import os
import argparse

import cherrypy

import jsonstore
from pastebin import (BASE, PasteBinPage, PasteViewPage, LastPage,
    PastePlainPage, FilePage, AboutPage)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest="configs",
        default=[], action="append", help="config file")
    return parser.parse_args()

def main():
    args = get_args()
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

    app = cherrypy.tree.mount(root=None)
    app.merge(app_conf)
    map(app.merge, args.configs)

    cherrypy.quickstart(None, '', config=app.config)

if __name__ == '__main__':
    '''
    Useful for development mode
    '''
    main()
