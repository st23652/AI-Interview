# watson_integration/urls.py
from django.urls import path
from .views import AIQuestionView

urlpatterns = [
    path('generate-question/', AIQuestionView.as_view(), name='generate-question'),
]
