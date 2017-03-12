import sys
import falcon
from requestlogger import WSGILogger, ApacheFormatter
from logging import StreamHandler
from outlet import middleware
from outlet import db
from outlet import resources


def make_app():
    outlet = resources.TransactionResource()
    client = resources.ClientResource()
    test = resources.TestResource()
    app = falcon.API(middleware=[middleware.JSONTranslator(),
                                 middleware.RequireJSON(),
                                 middleware.DBSessionManager(db.Session)])
    app.add_route('/', outlet)
    app.add_route('/test', test)
    app.add_route('/client-token', client)
    handlers = [StreamHandler(stream=sys.stdout)]
    return WSGILogger(app, handlers,
                      formatter=ApacheFormatter(), propagate=False)


app = make_app()
