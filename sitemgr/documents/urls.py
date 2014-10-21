from django.conf.urls import patterns, include, url
from documents.models import Document,Office,Tag
from django.views.generic import ListView,DetailView,CreateView,\
        UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from documents.views import HomeView
DOCUMENT_FIELDS=['code','year','number','name','tags','efficetive_date',\
    'expire_date']
LIST_URL=reverse_lazy('documents:home')
detail={
        'model':Document,
        }        
update={
        'model':Document,
        'fields':DOCUMENT_FIELDS,
        'success_url' : LIST_URL,
        }
delete={
        'model':Document,
        'template_name':'base_confirm_delete.html',
        'success_url':LIST_URL,
        }

urlpatterns = patterns('',
        url(r'^home/$',HomeView.as_view(),name='home'),
        url(r'(?P<pk>\d+)/update/$',UpdateView.as_view(**update),name='update'),
        url(r'(?P<pk>\d+)/delete/$',DeleteView.as_view(**delete),name='delete'),
        url(r'(?P<pk>\d+)/detail/$',DetailView.as_view(**detail),name='detail'),
)
