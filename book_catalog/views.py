from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from book_catalog.models import Book, BookCategory

class IndexView(TemplateView):
    template_name = 'book/index.html'
    title = 'Домашня сторінка'


class AboutBookView(DetailView):
    model = Book
    template_name = 'book/about_book.html'
    context_object_name = 'book'


class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    title = 'Book - Каталог'

    def get_queryset(self):
        queryset = super().get_queryset().filter(for_sale=True)
        category_id = self.request.GET.get('category_id')

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()

        category_id = self.request.GET.get('category_id')
        if category_id and category_id.isdigit():
            context['curent_category'] = BookCategory.objects.filter(id=category_id).first()
        return context