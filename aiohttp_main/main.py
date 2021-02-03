import aiohttp_jinja2
import jinja2
from aiohttp import web

from urls import urlpatterns


def run():
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('template'))
    app.add_routes(urlpatterns)
    web.run_app(app)


if __name__ == '__main__':
    run()
