from .models import DebugData
from debug_toolbar.middleware import DebugToolbarMiddleware
from django.core.urlresolvers import reverse, resolve, Resolver404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.static import serve
import thread

import urls as debug_panel_urlconf

debug_toolbar_process_request = DebugToolbarMiddleware.process_request


def process_request(self, request):
    try:
        res = resolve(request.path, urlconf=debug_panel_urlconf)
    except Resolver404:
        return debug_toolbar_process_request(self, request)

    return res.func(request, *res.args, **res.kwargs)


def process_response(self, request, response):
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

    stats = DebugData(data=toolbar.render_toolbar())
    stats.save()
    response['X-debug-data-url'] = request.build_absolute_uri(
        reverse('debug_data', urlconf=debug_panel_urlconf, kwargs={'id': stats.id}))

    del self.__class__.debug_toolbars[ident]
    return response

DebugToolbarMiddleware.process_response = process_response
DebugToolbarMiddleware.process_request = process_request
