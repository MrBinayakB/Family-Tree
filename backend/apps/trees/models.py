from django.db import models

class Trees(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=False)
    updated_at = models.DateTimeField(auto_now=True)
