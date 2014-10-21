from django.conf.urls import patterns, include, url
from report.views import HomeView,MonthReport,QuaterReport
from report.upload import UploadView
urlpatterns = patterns('',
        url(r'^home/$',HomeView.as_view(),name='home'),
        url(r'^monthrpt/$',MonthReport.as_view(),name='monthrpt'),
        url(r'^quaterrpt/$',QuaterReport.as_view(),name='quaterrpt'),
        url(r'^upload/$',UploadView.as_view(),name='upload'),
)
