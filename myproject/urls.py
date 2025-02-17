from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# View to render the home page
def home(request):
    return render(request, "home.html")  # Render your template here

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # Map root URL to home_view
    path("myapp/", include("myapp.urls")),  # Include URLs from myapp
]
