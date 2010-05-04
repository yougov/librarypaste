#!/usr/bin/env python
# encoding: utf-8

import os
import cherrypy
from pastebin import BASE, PasteBinPage, PasteViewPage, LastPage, PastePlainPage

def main():
    mapper = cherrypy.dispatch.RoutesDispatcher()
    mapper.connect('paste', '', PasteBinPage(),
                     action='post', conditions=dict(method=['POST']))
    mapper.connect('paste', '', PasteBinPage())
    mapper.connect('viewpaste', ':pasteid', PasteViewPage())
    mapper.connect('plain', 'plain/:pasteid', PastePlainPage())
    mapper.connect('last', 'last/:nick', LastPage())

    # Cherrypy configuration here
    app_conf = {
        '/' : {'request.dispatch' : mapper},
        '/static' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : os.path.join(BASE, 'static'),
        },
        'repo' : {'path' : os.path.join(os.getcwd(), 'repo')},
        'lexers' : {'favorites' : ['python']},
    }

    cherrypy.tree.mount(root=None, config=app_conf)
    cherrypy.quickstart(None, '', config=app_conf)

if __name__ == '__main__':
    '''
    Useful for development mode
    '''
    main()
    