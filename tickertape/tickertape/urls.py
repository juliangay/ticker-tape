from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tickertape.views.home', name='home'),
    # url(r'^tickertape/', include('tickertape.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^feeds/', include('feeds.urls')),
)

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()