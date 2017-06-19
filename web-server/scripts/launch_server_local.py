import os.path
import sys

import cherrypy

from webserver.server import CodenamesSolverApp

try:
    data_dir = sys.argv[1]
except IndexError:
    data_dir = "../data"

conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'webserver/public'
    }
}
cherrypy.quickstart(CodenamesSolverApp(data_dir), '/', conf)
