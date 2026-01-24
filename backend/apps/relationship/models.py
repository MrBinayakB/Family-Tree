from django.db import models

class relation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
