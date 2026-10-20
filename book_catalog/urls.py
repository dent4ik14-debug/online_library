from django.urls import path, include
from book_catalog.views import BookListView, AboutBookView, basket_add, basket_remove

app_name = 'book_catalog'

urlpatterns = [
    path('catalog/', BookListView.as_view(), name='catalog'),
    path('book/<int:pk>/', AboutBookView.as_view(), name='book_detail'),
    path('basket/add/<int:book_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove')
]