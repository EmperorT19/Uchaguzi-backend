from django.urls import path
from .views import *


urlpatterns = [
    path("timo", index),
    path("register", signup) 
    
]