from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<path:path>/', RedirectView.as_view(url='/static/media/')),  # Adjust for static serving

    # Add this line to route root requests
    path('', include('myapp.urls')),  # Assuming 'core.urls' includes a home view.
]
