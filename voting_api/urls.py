from django.urls import path
from .views import *

urlpatterns = [
    path("timo", index),
    path("register", signup),
    path("login", login),
    path("vote", cast_vote),
    path("candidates", get_candidates),
    path("results", get_results),
    path("voter/status", voter_status),
]