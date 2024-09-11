from django.urls import path
from .views import register, login_view, account, logout_view

urlpatterns = [
    path('register/', register, name='register'),  # Maps to the register view
    path('login/', login_view, name='login'),      # Maps to the login view
    path('account/', account, name='account'),     # Maps to the account view
    path('logout/', logout_view, name='logout'),   # Maps to the logout view
]