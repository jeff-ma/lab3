from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns =[
    # index / home page
    url(r'^$', views.index, name='index'),
    url(r'^expand/$', views.expand, name='expand'),
    url(r'^(?P<url_pk>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^url/$', views.url_listing),
	url(r'^url/(?P<pk>[0-9]+)/$', views.url_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)