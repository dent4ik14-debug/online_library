from django.contrib import admin
from django.urls import path
from book.views import book_list

app_name = 'book'

urlpatterns = [
    path('', book_list, name="book_list"),
]