import json

import aiohttp
import elasticsearch
from aiohttp import web
from elasticsearch import Elasticsearch

from parser import Parser

es = Elasticsearch()


async def parser_site(request):
    """
    Parsing the site.

    Data additions to django and elasticsearch.
    """
    content: bytes = await request.content.read()
    parser = Parser(content=content)

    if parser.error:
        return web.json_response(data=parser.error)

    async with aiohttp.ClientSession() as session:
        async with session.get(parser.url) as response:
            html: str = await response.text()
            parser.pars_html(html=html)

            async with session.get('http://localhost:8000/api/add-site',
                                   json=parser.result) as _:  # Data additions to django
                json_response = json.loads(await _.text())
                async with session.get(f'http://localhost:8000/api/site-detail-elastic/'  # Get data
                                       f'{json_response["site_id"]}?format=json') as site_response:
                    await site_response.text()
                    print(f'http://localhost:8000/api/api/site-detail-elastic/'  # Get data
                          f'{json_response["site_id"]}?format=json')
                    json_site = json.loads(await site_response.text())
                    try:
                        es.index(index="site", id=json_site['site']['id'],
                                 body=json_site)  # Data additions to elasticsearch
                    except elasticsearch.exceptions.ConflictError:
                        try:
                            es.update(index="site", id=json_site['site']['id'],
                                      body=json_site)  # Data update to elasticsearch
                        except elasticsearch.exceptions.RequestError:
                            es.delete(index="site", id=json_site['site']['id'])
                            es.index(index="site", id=json_site['site']['id'],
                                     body=json_site)  # Data additions to elasticsearch
                return web.json_response(data={'ok': 'add data'})
