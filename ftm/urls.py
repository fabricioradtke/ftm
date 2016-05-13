from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',

    url(r'^$',                         'home.views.home',       name='home'),
    url(r'^movie/(?P<id>\d+)/$',       'detail.views.detail',   name='detail'),
    url(r'^search/(?P<query>[^/]+)/$', 'search.views.search',   name='search'),
    url(r'^explore/',                  'explore.views.explore', name='explore'),
)

urlpatterns += patterns('',
	url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += staticfiles_urlpatterns()
