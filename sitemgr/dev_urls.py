from django.conf.urls import patterns, include, url
from django.contrib import admin
from sitemgr.dev_settings import INSTALLED_APPS

pattern_list=[
    '',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
              ]

for app in INSTALLED_APPS:
    if not app.startswith('django.contrib'):
        pattern_list.append(url('^%s/'%(app),include("%s.urls"%(app),
            namespace=app)))

urlpatterns = patterns(*pattern_list)
