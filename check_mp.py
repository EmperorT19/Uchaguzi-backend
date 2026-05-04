import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

from voting_api.models import Seat, Voter

# Check MP seats
mp_count = Seat.objects.filter(seat_type='mp').count()
print(f"Total MP seats: {mp_count}")

if mp_count > 0:
    sample = Seat.objects.filter(seat_type='mp')[:3]
    for s in sample:
        cand_count = s.candidates.count()
        print(f"  MP Seat id={s.id} name={s.name} level={s.level} constituency={s.constituency} candidates={cand_count}")
else:
    print("  NO MP seats found in DB!")

# Check all seat types
print("\nSeat type breakdown:")
from django.db.models import Count
for row in Seat.objects.values('seat_type').annotate(cnt=Count('id')):
    print(f"  {row['seat_type']}: {row['cnt']}")

# Check a voter
v = Voter.objects.first()
if v:
    print(f"\nSample voter: county={v.county} constituency={v.constituency} ward={v.ward}")
