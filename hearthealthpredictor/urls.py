from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predictor/', include('predictor.urls')),  # Include URLs from predictor app
    path('', include('predictor.urls')),  # Redirect root URL to predictor app
]
