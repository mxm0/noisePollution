from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^checkMessages/$', views.check_messages, name='check_messages'),
    url(r'^addDevice/$', views.add_device, name='add_device'),
    url(r'^deviceList/$', views.list_device, name='list_device'),
    url(r'^graph/(?P<deveui>.+)/$', views.graph, name='graph'),
    url(r'^deviceSearch/$', views.ajax_device_search, name = 'device_search' ),
    url(r'^editDevice/(?P<deveui>.+)/$', views.edit_device, name = 'edit_device' ),
    url(r'^deleteDevice/(?P<deveui>.+)/$', views.delete_device, name = 'delete_device' ),
    url(r'^map/$', views.map, name='map'),
    url(r'^about/$', views.about, name='about'),
    url(r'^logout/$', auth_views.logout, name="logout", kwargs={'next_page': 'index'}),
    url(r'^login/$', auth_views.login, name="login")
]