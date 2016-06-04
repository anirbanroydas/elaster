from tornado import web
from tornado.web import URLSpec as url
from sockjs.tornado import SockJSRouter

from settings import settings
from utils import include
from apps.main.views import SearchSockjsHandler


# Register SocjJsRouter Connection
SockjsWebsocketRouter = SockJSRouter(SearchSockjsHandler, '/sockjs_search')

urls = [
    url(r"/static/(.*)", web.StaticFileHandler,
        {"path": settings.get('static_path')}),
]

urls += include(r"/", "apps.main.urls")

urls = urls + SockjsWebsocketRouter.urls
