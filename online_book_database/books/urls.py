from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_book, name='add_book'),
    path('account/', views.account, name='account'),
    path('add_review/', views.add_review, name='add_review'),
    path('remove/<int:book_id>/', views.remove_book, name='remove_book'),
    path('book/<int:book_id>/', views.book_details, name='book_details'),
    path('update/<int:book_id>/', views.update_book, name='update_book'),
]