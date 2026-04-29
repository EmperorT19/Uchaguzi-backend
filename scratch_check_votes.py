import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

from voting_api.models import Vote, Seat, Candidate

print(f"Total Votes: {Vote.objects.count()}")

print("\nVotes by Seat Type:")
for stype in ['president', 'governor', 'senator', 'mp', 'woman_rep', 'mca']:
    count = Vote.objects.filter(seat__seat_type=stype).count()
    print(f"{stype}: {count}")

print("\nLast 5 Votes Details:")
for v in Vote.objects.all().order_by('-id')[:5]:
    print(f"ID={v.id} Voter={v.voter_id} Seat={v.seat.seat_type} ({v.seat.name}) Candidate={v.candidate.full_name}")
