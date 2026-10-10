from django.shortcuts import render
from book.models import Book
# Create your views here.
def book_list(request):
    context = {
        'title': 'Каталог',
        'books': Book.objects.all()
    }
    return render(request, 'book/book_list.html', context)