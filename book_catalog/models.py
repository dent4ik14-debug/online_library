from django.db import models

# Create your models here.
class BookCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    for_sale = models.BooleanField(default=True)
    category = models.ForeignKey(to=BookCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Назва:{self.name}'