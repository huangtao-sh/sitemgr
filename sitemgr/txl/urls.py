from django.conf.urls import patterns, include, url
from txl.models import Address
from django.views.generic import ListView,DetailView,CreateView,\
        UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from txl.views import HomeView,Search
ADDRESS_FIELDS=['name','company','department','mobile',\
    'tel','email','memo']
LIST_URL=reverse_lazy('txl:home')
create={
        'model':Address,
        'fields':ADDRESS_FIELDS,
        'success_url':LIST_URL
        }
detail={
        'model':Address,
        }        
update={
        'model':Address,
        'fields':ADDRESS_FIELDS,
        'success_url' : LIST_URL,
        }
delete={
        'model':Address,
        'template_name':'base_confirm_delete.html',
        'success_url':LIST_URL,
        }
urlpatterns = patterns('',
    url(r'^home/$',HomeView.as_view(),name='home'),
    url(r'^search/$',Search.as_view(),name='search'),
    url(r'^create/$',CreateView.as_view(**create),name='create'),
    url(r'(?P<pk>\d+)/update/$',UpdateView.as_view(**update),name='update'),
    url(r'(?P<pk>\d+)/delete/$',DeleteView.as_view(**delete),name='delete'),
    url(r'(?P<pk>\d+)/detail/$',DetailView.as_view(**detail),name='detail'),
#    url(r'^create/$',CreateView,{'model':Address}),
)
