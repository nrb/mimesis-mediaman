from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^edit/$', 'mediaman.tests.exampleapp.views.edit'),
    (r'^edit/(\d+)/$', 'mediaman.tests.exampleapp.views.edit'),
    (r'^list/$', 'mediaman.tests.exampleapp.views.list'),
    (r'^mediaman/', include('mediaman.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )
