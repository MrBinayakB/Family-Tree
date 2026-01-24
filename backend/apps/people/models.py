from django.db import models

# Create your models here.
class PeopleModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, null=False)
    familyname = models.CharField(max_length=100, null=False)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)