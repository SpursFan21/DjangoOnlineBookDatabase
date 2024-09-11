from django.urls import path
from .views import add_book
from . import views

urlpatterns = [
    path('add_book/', add_book, name='add_book'),
    path('add_review/', views.add_review, name='add_review'),
]
