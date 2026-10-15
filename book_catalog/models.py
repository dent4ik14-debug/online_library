from django.db import models
from users.models import CustomUser
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
    image = models.ImageField(upload_to='books_images/', null=True, blank=True)
    for_sale = models.BooleanField(default=True)
    category = models.ForeignKey(to=BookCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Назва:{self.name}'

    
class BasketQuerySet(models.query.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    quantity = models.PositiveSmallIntegerField(default=0)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.email} | Продукт: {self.product.name}"

    def sum(self):
        return self.quantity * self.book.price