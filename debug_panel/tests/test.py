from __future__ import absolute_import, unicode_literals

import threading

from urlparse import urlparse

from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from debug_panel.middleware import DebugPanelMiddleware


rf = RequestFactory()
debug_url_header_key = 'X-debug-data-url'


@override_settings(DEBUG=True)
class DebugPanelTestCase(TestCase):
    def setUp(self):
        request = rf.get('/')
        response = HttpResponse()

        self.middleware = DebugPanelMiddleware()
        self.request = request
        self.response = response


    def _get_toolbar(self):
        return DebugPanelMiddleware.debug_toolbars[threading.current_thread().ident]

    def _set_toolbar(self, toolbar):
        DebugPanelMiddleware.debug_toolbars[threading.current_thread().ident] = toolbar

    def assertValidDebugHeader(self, response):
        self.assertIn(debug_url_header_key, response)


    def assertNoDebugHeader(self, response):
        self.assertNotIn(debug_url_header_key, response)


    def test_appends_header(self):
        self.middleware.process_request(self.request)
        self.middleware.process_response(self.request, self.response)

        self.assertValidDebugHeader(self.response)


    def test_appends_header_on_ajax_request(self):
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        self.middleware.process_request(self.request)
        self.middleware.process_response(self.request, self.response)

        self.assertValidDebugHeader(self.response)


    def test_debug_url_is_fully_qualified(self):
        """
        since the debug url might be resolved from a different hostname,
        inside a chrome devkit panel for example, the url must be fully
        qualified.
        """
        self.middleware.process_request(self.request)
        self.middleware.process_response(self.request, self.response)

        debug_url = self.response[debug_url_header_key]
        self.assertTrue(debug_url.startswith('http://testserver/'))


    def test_debug_view_render_toolbar(self):
        self.middleware.process_request(self.request)

        # store the toolbar before it's deleted by the middleware
        toolbar = self._get_toolbar()
        self.middleware.process_response(self.request, self.response)

        debug_url = self.response[debug_url_header_key]
        response = self.client.get(urlparse(debug_url).path)
        self.assertEqual(response.status_code, 200)

        # the toolbar must be set in DebugPanelMiddleware to be rendered
        self._set_toolbar(toolbar)
        self.assertEqual(response.content, toolbar.render_toolbar())


    def test_debug_view_frame_friendly(self):
        """
        Clickjacking protection must be disable for the debug view
        since it must be callable inside iframe.
        """
        self.middleware.process_request(self.request)
        self.middleware.process_response(self.request, self.response)

        debug_url = self.response[debug_url_header_key]
        response = self.client.get(urlparse(debug_url).path)

        self.assertNotIn('X-Frame-Options', response)
