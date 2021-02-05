from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import json

from .models import Company, Site, Keyword
from .serializers import SiteSerializer, SiteElasticsearchSerializer


def add_site(requests):
    json_parser = json.loads(requests.body)

    try:
        company = Company.objects.get(domain=json_parser['company']['domain'])
    except Company.DoesNotExist:
        company = Company(**json_parser['company'], request=1)
        if not company.name:
            company.name = '.'.join(company.domain.split('.')[0:-1])
        company.save()

    if not company.name and 'name' in json_parser['company']:
        company.name = json_parser['company']['name']
        company.save()
    if company:
        company.request += 1
        company.save()

    try:
        site = Site.objects.get(url=json_parser['site']['url'])
        site.request += 1
        site.save()
    except Site.DoesNotExist:
        site = Site(**json_parser['site'], company=company, request=1)
        site.save()

    for key in json_parser['keywords']:
        try:
            Keyword.objects.get(key=key)
        except Keyword.DoesNotExist:
            keyword = Keyword(key=key, request=1)
            keyword.save()
            keyword.site.add(site)
            keyword.save()
    return JsonResponse({'site_id': site.id})


class SiteView(APIView):
    def get(self, request, id_site=None):
        if not id_site:
            sites = Site.objects.all()
            serializer = SiteSerializer(sites, many=True)
            return Response({"site": serializer.data})

        sites = Site.objects.get(id=id_site)
        serializer = SiteSerializer(sites)

        data = serializer.data
        data['keyword'] = []
        for key in sites.keyword_set.all():
            data['keyword'].append(key.key)
        return Response({"site": data})


class SiteElasticsearchView(APIView):
    def get(self, request, id_site):
        sites = Site.objects.get(id=id_site)
        serializer = SiteElasticsearchSerializer(sites)

        data = serializer.data
        data['keyword'] = []
        for key in sites.keyword_set.all():
            data['keyword'].append(key.key)
        return Response({"site": data})
