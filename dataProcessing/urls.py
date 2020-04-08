# pages/urls.py
from django.urls import path

from .views import DataProcessingView

urlpatterns = [
    path('', DataProcessingView, name='dataProcessingView')
]
