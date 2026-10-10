from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=64)
    deskription = models.CharField(max_length=256, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    price = models.DecimalField()
    for_sale = models.BooleanField(default=True)
    def __str__(self):
        return f'Name:{self.name}'