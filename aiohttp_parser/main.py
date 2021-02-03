from aiohttp import web

from urls import urlpatterns


def run():
    app = web.Application()
    app.add_routes(urlpatterns)
    web.run_app(app, port=9000)


if __name__ == '__main__':
    run()
