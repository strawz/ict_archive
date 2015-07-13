from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^api/$', views.api_root),
    url(r'^api/check-md5/$', views.api_check_md5, name='api-check-md5'),
    url(r'^api/files/$', views.ApiArchiveFileList.as_view(),
        name='api-archivefile-list'),
    url(r'^api/files/(?P<pk>[0-9]+)/$', views.ApiArchiveFileDetail.as_view(),
        name='api-archivefile-detail'),
    url(r'^api/users/$', views.ApiUserList.as_view(),
        name='api-user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.ApiUserDetail.as_view(),
        name='api-user-detail'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArchiveFileDetailView.as_view(), name='achivefile-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
