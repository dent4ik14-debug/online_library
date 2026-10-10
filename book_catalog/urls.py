from django.urls import path, include
from book_catalog.views import BookListView

app_name = 'book_catalog'

urlpatterns = [
    path('catalog/', BookListView.as_view(), name='catalog')
]