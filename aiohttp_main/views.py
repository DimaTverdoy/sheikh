from pprint import pprint

import aiohttp
import aiohttp_jinja2
import wikipya
from aiohttp import web
from wikipya.aiowiki import Wikipya
from elasticsearch import Elasticsearch

import json

wiki = Wikipya("ru")
es = Elasticsearch()


async def search_sites(request):
    """
    Search sites in elasticsearch.

    Search all fields. Index site.
    """
    if 'search' in request.rel_url.query:   # Parameter check search
        if not request.rel_url.query['search']:
            return web.json_response({'Error': 'not found search param'})

    search = es.search(body={"query": {"query_string": {"query": request.rel_url.query['search']}}}, index='site')
    return web.json_response(search['hits']['hits'])


async def index(request):
    """
    If there is a parameter search then the search page.
    Else the main page.
    """
    if 'search' in request.rel_url.query:
        return aiohttp_jinja2.render_template('search.html', request, {})
    else:
        return aiohttp_jinja2.render_template('index.html', request, {})


async def search_wiki(request):
    """
    Finding information in Wikipedia.

    https://ru.wikipedia.org/
    https://github.com/jDan735/wikipya
    """
    result: dict = dict()
    if 'search' in request.rel_url.query:
        if not request.rel_url.query['search']:
            return web.json_response({'Error': 'not found wiki page'})
        try:
            search_wiki_responses = await wiki.search(request.rel_url.query['search'])
        except wikipya.aiowiki.NotFound:
            searches = await wiki.opensearch(request.rel_url.query['search'])
            try:
                search_wiki_responses = await wiki.search(searches[1][0])
            except IndexError:
                return web.json_response({'Error': 'not found wiki page'})
        stat = await wiki.page(search_wiki_responses[0])

        result['title'] = stat.title
        result['summary'] = stat.fixed
        try:
            images = await stat.image()
        except wikipya.aiowiki.NotFound:
            result['img'] = ''
        else:
            result['img'] = images.source

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://ru.wikipedia.org/w/api.php?action=query&prop=info&pageids='
                    f'{stat.pageid}&inprop=url&format=json') as response:
                json_wiki = await response.text()
                json_wiki = json.loads(json_wiki)
                result['url'] = json_wiki['query']['pages'][str(stat.pageid)]['fullurl']

        if len(result['summary']) > 500:    # Description limitation
            result['summary'] = result['summary'][0:500] + '...'
    else:
        return web.json_response({'Error': 'not param search'})

    return web.json_response(data=result)


async def add_site(request):
    """
    Site additions.

    Request in django.
    """
    data = await request.post()
    if 'site' in data:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://127.0.0.1:9000/add-site', json={'url': data['site']}) as response:
                await response.text()
    return aiohttp_jinja2.render_template('search.html', request, {})
