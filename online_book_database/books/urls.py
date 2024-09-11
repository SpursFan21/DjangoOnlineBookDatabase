from django.urls import path
from . import views

urlpatterns = [
    # Placeholder path
    path('', views.index, name='books_index'),
]
