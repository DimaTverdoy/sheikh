from django.urls import path

from .views import add_site, SiteView, SiteElasticsearchView

app_name = 'api'
urlpatterns = [
    path('add-site/', add_site, name='add_site'),
    path('site-detail/', SiteView.as_view(), name='site-detail'),
    path('site-detail/<int:id_site>', SiteView.as_view(), name='site-detail'),
    path('site-detail-elastic/<int:id_site>', SiteElasticsearchView.as_view(), name='site-detail-elastic')
]
