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
    path("voter/change-password", change_password),
    path("candidate/summarize", summarize_candidate),
    path("system-admin/login", admin_login),
    path("system-admin/stats", admin_stats),
    path("system-admin/voters", admin_voters),
    path("system-admin/candidates", admin_candidates),
    path("system-admin/votes", admin_votes),
    path("system-admin/toggle-halt", admin_toggle_halt),
    path("system-admin/candidates/add", admin_candidate_add),
    path("system-admin/candidates/<int:id>/delete", admin_candidate_delete),
    path("system-admin/restart-voting", admin_restart_election),
]