from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from online_book_database.views import home
from accounts.views import login_view, register  # Import the views for login and register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register, name='register'),  # Register page URL
    path('accounts/login/', login_view, name='login'),      # Login page URL
    path('accounts/', include('accounts.urls')),  # Includes the accounts app URLs
    path('books/', include('books.urls')),        # Includes the books app URLs
    path('api/', include('api.urls')),             # Includes the API app URLs
    path('', home, name='home'),  # Root URL pattern
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
