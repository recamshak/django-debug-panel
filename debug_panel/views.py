from django.http import HttpResponse
from .cache import cache
from django.shortcuts import render_to_response
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def debug_data(request, cache_key):
    html = cache.get(cache_key)

    if html is None:
        return render_to_response('debug-data-unavailable.html')

    return HttpResponse(html, content_type="text/html")
