from django.contrib import admin
from django.contrib import admin
from .models import Seat, Candidate, Voter, Vote

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['name', 'seat_type', 'level', 'county', 'constituency', 'ward']
    list_filter = ['seat_type', 'level']
    search_fields = ['name']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'party', 'seat']
    list_filter = ['seat__seat_type']
    search_fields = ['full_name', 'party']

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'id_number', 'county', 'constituency', 'ward']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'seat', 'candidate', 'voted_at']
# Register your models here.
