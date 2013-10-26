"""
URLpatterns for the debug panel.

These should not be loaded explicitly; It is used internally by the
debug-panel application.
"""
try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url

_PREFIX = '__debug__'

urlpatterns = patterns('debug_panel.views',
    url(r'^%s/data/(?P<cache_key>\d+\.\d+)/$' % _PREFIX, 'debug_data', name='debug_data'),
)
