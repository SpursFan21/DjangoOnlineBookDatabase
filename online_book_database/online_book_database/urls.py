from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # Your existing app URLs
    path('accounts/', include('accounts.urls')),  # Include accounts URLs
]
