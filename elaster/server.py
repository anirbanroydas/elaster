import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options
import logging
import os.path

from urls import urls
from settings import settings


define("port", default=9091, help="run on the given port", type=int)
define("example", default='webapp', help='the example app to run in elaster server', type=str)


LOGGER = logging.getLogger(__name__)


class Application(tornado.web.Application):

    def __init__(self, example):
        tpath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'examples', example))
        spath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'examples', example, 'static'))

        settings['template_path'] = tpath
        settings['static_path'] = spath

        tornado.web.Application.__init__(self, urls, **settings)



def main():
    tornado.options.parse_command_line()
    app = Application(options.example)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    LOGGER.info('[server.main] Starting Elaster on http://127.0.0.1:%s', options.port)

    try:
        LOGGER.info("\n[server.main] Elaster server Started.\n")

        tornado.ioloop.IOLoop.current().start()
        
    except KeyboardInterrupt:
        LOGGER.error('\n[server.main] EXCEPTION KEYBOARDINTERRUPT INITIATED\n')
        LOGGER.info("[server.main] Stopping Server....")
        LOGGER.info('[server.main] closing all websocket connections objects and corresponsding mqtt client objects')
        LOGGER.info('Stopping elaster\'s Tornado\'s main iolooop')
        
        # Stopping main thread's ioloop, not to be confused with current thread's ioloop
        # which is ioloop.IOLoop.current()
        tornado.ioloop.IOLoop.instance().stop()

        LOGGER.info("\n[server.main] Elaster server Stopped.")


if __name__ == "__main__":
    main()
