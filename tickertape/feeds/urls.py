from django.conf.urls import *
from django.views.generic import TemplateView
from views import *

urlpatterns = patterns('',
    url(r'^entries$', entries, name='entries'),
    url(r'^pull$', pull_feeds, name='pull'),
    url(r'^upload$', upload_opml_file, name='upload'),
)