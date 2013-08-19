from django.db import models, transaction, DatabaseError

class DebugData(models.Model):
    data = models.TextField(null=False, blank=True)

    @staticmethod
    @transaction.commit_on_success
    def clear():
            DebugData.objects.all().delete()

try:
    DebugData.clear()
except DatabaseError:
    pass
