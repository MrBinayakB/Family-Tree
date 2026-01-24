from django.db import models

class Relation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    metadata_json = models.JSONField(null=True, blank=True)