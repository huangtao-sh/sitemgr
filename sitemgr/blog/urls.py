#  urls.py
#  
#  Copyright 2014 huangtao <huangtao.jh@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from django.conf.urls import patterns, include, url
from blog.views import BlogCreate,BlogUpdate,BlogDelete,\
    HomeView,BlogDetail

urlpatterns = patterns('',
    url(r'^create/$',BlogCreate.as_view(),name='create'),
    url(r'^home/$',HomeView.as_view(),name='home'),
    url(r'(?P<pk>\d+)/update/$',BlogUpdate.as_view(),name='update'),
    url(r'(?P<pk>\d+)/delete/$',BlogDelete.as_view(),name='delete'),
    url(r'(?P<pk>\d+)/detail/$',BlogDetail.as_view(),name='detail'),
)
