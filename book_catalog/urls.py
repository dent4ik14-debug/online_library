from django.urls import path, include
from book_catalog.views import BookListView, AboutBookView

app_name = 'book_catalog'

urlpatterns = [
    path('catalog/', BookListView.as_view(), name='catalog'),
    path('book/<int:pk>/', AboutBookView.as_view(), name='book_detail'),
]