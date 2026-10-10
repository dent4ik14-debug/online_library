from django.contrib import admin
from book_catalog.models import Book, BookCategory
# Register your models here.
admin.site.register(BookCategory)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')