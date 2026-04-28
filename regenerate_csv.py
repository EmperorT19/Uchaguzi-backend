import os
import sys
import django
import csv

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

# 1. Run the existing population script to generate all 8,000+ candidates locally
print("1. Generating Candidates into local SQLite DB...")
try:
    import populate_realistic_candidates
except Exception as e:
    print(f"Error running populate script: {e}")
    sys.exit(1)

from voting_api.models import Candidate

# 2. Dump the fully populated database to test_candidates.csv
print("\n2. Dumping fully generated candidates to test_candidates.csv...")
candidates = Candidate.objects.select_related('seat').all()

with open('test_candidates.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['full_name', 'party', 'seat_type', 'level', 'county_id', 'constituency_id', 'ward_id'])
    
    for c in candidates:
        writer.writerow([
            c.full_name,
            c.party,
            c.seat.seat_type,
            c.seat.level,
            c.seat.county if c.seat.county is not None else '',
            c.seat.constituency if c.seat.constituency is not None else '',
            c.seat.ward if c.seat.ward is not None else ''
        ])

print(f"SUCCESS! test_candidates.csv has been updated with {candidates.count()} candidates (including Governors, Senators, etc.).")
print("You can now commit and push this updated CSV to GitHub.")
