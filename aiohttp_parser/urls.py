from aiohttp import web

from views import parser_site


urlpatterns = [
    web.post('/add-site', parser_site),
]
