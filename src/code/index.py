import os
import sys

# Put sqlite_web on our python-path.
cur_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.realpath(os.path.join(cur_dir, '../code/sqlite_web')))

from sqlite_web import app
from sqlite_web import initialize_app, initialize_database


def handler(environ, start_response):
    app.config["env"] = environ
    app.config["context"] = environ["fc.context"]
    app.config["creds"] = app.config["context"].credentials
    initialize_app(environ["sqliteWebPassword"], environ["sqliteWebPrefix"])
    initialize_database("default.db")
    return app(environ, start_response)


if __name__ == '__main__':
    # Example showing how to run sqlite-web with a different WSGI server.
    from gevent import monkey ; monkey.patch_all()
    from gevent.pool import Pool
    from gevent.pywsgi import WSGIServer
    initialize_app("hello,world")
    initialize_database("default.db")
    pool = Pool(50)
    server = WSGIServer(('127.0.0.1', 8080), app, log=None, spawn=pool)
    server.serve_forever()
