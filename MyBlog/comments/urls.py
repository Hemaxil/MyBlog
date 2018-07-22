from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .views import *

#always put app_name
app_name='Blog'
urlpatterns = [
    #url(r'^details/(?P<slug>[\w-]+)/delete',post_delete,name='delete'),
    url(r'^(?P<id>\d+)',comment_thread,name="thread"),
]
# defining path for static files to be stored
