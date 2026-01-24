from django.db import models

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=32, null=False)