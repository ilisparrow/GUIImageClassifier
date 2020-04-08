# pages/urls.py
from django.urls import path

from .views import PictureTakerView
from .views import PictureTakerViewSecond

urlpatterns = [
    #path('', PictureTakerViewSecond),
    path('', PictureTakerView),


]
