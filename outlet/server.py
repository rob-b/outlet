import os
import sys
import falcon
from requestlogger import WSGILogger, ApacheFormatter
from logging import StreamHandler


def make_app():
    try:
        os.environ['DB_URL']
    except KeyError:
        print("You must set DB_URL environment variable")
        return

    # we don't try to import anything that relies on session until after we've
    # confirmed the required envvar exists
    from outlet import db
    from outlet import middleware
    from outlet import resources

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
