from tornado.web import URLSpec as url
from elaster.apps.main.views import IndexHandler, SearchHandler

urls = [
    url(r"/", IndexHandler),
    url(r"/search", SearchHandler)
]
