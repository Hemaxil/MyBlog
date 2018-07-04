from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .views import *

#always put app_name
app_name='Blog'
urlpatterns = [
    url(r'^$',post_list,name="lists"),
    url(r'^create',post_create,name='create'),
    #url(r'^details/(?P<id>\d+)/update',post_update,name="update"),
    url(r'^details/(?P<slug>[\w-]+)/update',post_update,name="update"),
    url(r'^details/(?P<slug>[\w-]+)/delete',post_delete,name='delete'),
    #passing id parameter in detail   detail/id
    #need to add app_name in urls in Blog --for namespace
    url(r'^details/(?P<slug>[\w-]+)',post_detail,name="details"),
]
# defining path for static files to be stored
