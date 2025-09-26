# pawfect/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/', include('adminpanel.urls')),  # ← include adminpanel app URLs
    path('', include('client.urls')),  # ← client app URLs
]
