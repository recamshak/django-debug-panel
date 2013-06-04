from django.db import models

class DebugData(models.Model):
	data = models.TextField(null=False, blank=True)

try:
	DebugData.objects.all().delete()
except:
	pass