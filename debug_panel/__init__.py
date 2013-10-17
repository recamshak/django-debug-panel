from debug_toolbar.middleware import DebugToolbarMiddleware
from django.core.urlresolvers import reverse, resolve, Resolver404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.static import serve
import thread
import time
from .cache import cache

# the urls patterns that concern only the debug_panel application
import urls as debug_panel_urlconf

debug_toolbar_process_request = DebugToolbarMiddleware.process_request

def process_request(self, request):
    """
    Try to match the request with an URL from debug_panel application.

    If it matches, that means we are serving a view from debug_panel,
    and we can skip the debug_toolbar middleware.

    Otherwise we fallback to the default debug_toolbar middleware.
    """

    try:
        res = resolve(request.path, urlconf=debug_panel_urlconf)
    except Resolver404:
        return debug_toolbar_process_request(self, request)

    return res.func(request, *res.args, **res.kwargs)


def process_response(self, request, response):
    """
    Since there is no hook to intercept and change rendering of the default
    debug_toolbar middleware, this is mostly a copy the original debug_toolbar
    middleware.

    Instead of rendering the debug_toolbar inside the response HTML, it stored
    in the Django cache.

    The data stored in the cache are then reachable from an URL that is appened
    to the HTTP response header under the 'X-debug-data-url' key.

    """

    __traceback_hide__ = True

    ident = thread.get_ident()
    toolbar = self.__class__.debug_toolbars.get(ident)

    try:
        current_view = resolve(request.path)[0]
    except Resolver404:
        current_view = None

    if current_view == serve or not toolbar:
        return response

    if isinstance(response, HttpResponseRedirect):
        if not toolbar.config['INTERCEPT_REDIRECTS']:
            return response

        redirect_to = response.get('Location', None)
        if redirect_to:
            cookies = response.cookies
            response = render_to_response(
                'debug_toolbar/redirect.html',
                {'redirect_to': redirect_to}
            )
            response.cookies = cookies

    for panel in toolbar.panels:
        panel.process_response(request, response)

    cache_key = "%f" % time.time()
    cache.set(cache_key, toolbar.render_toolbar())

    response['X-debug-data-url'] = request.build_absolute_uri(
        reverse('debug_data', urlconf=debug_panel_urlconf, kwargs={'cache_key': cache_key}))

    del self.__class__.debug_toolbars[ident]
    return response

DebugToolbarMiddleware.process_response = process_response
DebugToolbarMiddleware.process_request = process_request
