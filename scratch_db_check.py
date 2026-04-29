import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

from voting_api.models import Seat, Vote, Candidate, Voter

print(f"Voters: {Voter.objects.count()}")
print(f"Seats: {Seat.objects.count()}")
print(f"Candidates: {Candidate.objects.count()}")
print(f"Votes: {Vote.objects.count()}")

print("\nFirst 10 Seats:")
for s in Seat.objects.all()[:10]:
    print(f"{s.id}: {s.name} ({s.seat_type}) Level={s.level} C={s.county} CN={s.constituency} W={s.ward}")

print("\nFirst 5 Votes:")
for v in Vote.objects.all()[:5]:
    print(f"Voter {v.voter.id} voted for {v.candidate.full_name} in seat {v.seat.id} ({v.seat.seat_type})")
