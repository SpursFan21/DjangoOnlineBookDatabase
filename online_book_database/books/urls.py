from django.urls import path
from .views import add_book

urlpatterns = [
    path('add_book/', add_book, name='add_book'),
]
