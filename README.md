==================
Django Debug Panel
==================

Django Debug Toolbar inside WebKit DevTools. Works fine with background AJAX requests and non-HTML responses.
Great for single-page applications and other AJAX intensive web applications.

Installation
============

1. Install and configure [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar>)

2. Add `debug_panel` to your `INSTALLED_APPS` setting::

       INSTALLED_APPS = (
           ...
           'debug_panel',
       )

3. Run `python manage.py syncdb` to create the table that store debug information

4. Install the Chrome extension Django-panel