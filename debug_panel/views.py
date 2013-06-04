from .models import DebugData
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def debug_data(request, id):
	html = get_object_or_404(DebugData, id=id).data
	return HttpResponse(html, content_type="text/html")
