from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'register$', views.register, name='register'),
    url(r'login$', views.login, name='login'),
    url(r'search$', views.search, name='search'),
    url(r'logout$', views.logout, name='logout'),
    url(r'user$', views.user, name='user'),
    url(r'admin$', views.admin, name='admin'),
    url(r'app/([^/]+)$', views.app, name='app'),
    url(r'dis/([^/]+)$', views.dis, name='dis'),
    url(r'blk/([^/]+)$', views.blk, name='blk'),
    url(r'unb/([^/]+)$', views.unb, name='unb'),
    url(r'delete/([^/]+)$', views.delete, name='delete'),
    url(r'node_decode/(.+)$', views.node_decode, name='node_decode'),
    url(r'^.*/$', views.home, name='home')
]
