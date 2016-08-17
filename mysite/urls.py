from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^accounts/login/$', views.login, name='login'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout', kwargs={'next_page': '/expander3'}), 
	url(r'', include('urlexpander3.urls')),
]