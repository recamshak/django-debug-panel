"""
URLpatterns for the debug toolbar.

These should not be loaded explicitly; the debug toolbar middleware will patch
this into the urlconf for the request.
"""
try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url

_PREFIX = '__debug__'

urlpatterns = patterns('debug_panel.views',
    url(r'^%s/data/(?P<id>\d+)/$' % _PREFIX, 'debug_data', name='debug_data'),
)