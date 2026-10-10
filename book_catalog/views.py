from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from book_catalog.models import Book

class IndexView(TemplateView):
    template_name = 'book/index.html'
    title = 'Домашня сторінка'


class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    title = 'Book - Каталог'
