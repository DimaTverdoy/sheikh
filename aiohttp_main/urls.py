from aiohttp import web

from views import index, search_wiki, add_site, search_sites

urlpatterns = [
    web.get('/', index),
    web.get('/wiki', search_wiki),
    web.post('/', add_site),
    web.get('/search-site', search_sites)
]
