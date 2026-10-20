from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from book_catalog.models import Book, BookCategory, Basket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q

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

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        category_id = self.request.GET.get('category_id')
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=category_id)

        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        if sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        if sort_by == 'newest':
            queryset = queryset.order_by('-id')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()

        category_id = self.request.GET.get('category_id')
        if category_id and category_id.isdigit():
            context['curent_category'] = BookCategory.objects.filter(id=category_id).first()
        return context


@login_required
def basket_add(request, book_id):
    book = Book.objects.get(id=book_id)
    baskets = Basket.objects.filter(user=request.user, book=book)
    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])