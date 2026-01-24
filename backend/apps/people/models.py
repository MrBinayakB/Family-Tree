from django.db import models
from trees.models import Trees
class People(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, null=False)
    familyname = models.CharField(max_length=100, null=False)
    birth_date = models.DateField()
    is_living = models.BooleanField()
    death_date = models.DateField()
    gender = models.CharField(max_length=10)
    tree = models.ForeignKey(Trees, on_delete=models.CASCADE)