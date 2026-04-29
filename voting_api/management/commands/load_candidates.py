# Optimized Candidate Seeding Script: 
# Uses bulk_create to import thousands of regional candidates without database timeouts.
# PRESERVES existing seats and candidates where possible to avoid breaking vote integrity.
import csv
import os
from django.core.management.base import BaseCommand
from voting_api.models import Candidate, Seat, Vote

class Command(BaseCommand):
    help = 'Load candidates from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The absolute or relative path to the CSV file')
        parser.add_argument('--force', action='store_true', help='Wipe only if absolutely necessary')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        force = kwargs.get('force', False)

        if not os.path.exists(csv_file):
            self.stderr.write(f"File not found: {csv_file}")
            return

        if force:
            # We only wipe if there are NO votes. If there are votes, we protect them.
            vote_count = Vote.objects.count()
            if vote_count > 0:
                self.stdout.write(self.style.WARNING(f"Database has {vote_count} votes. Skipping total wipe to preserve integrity."))
                self.stdout.write("Instead, we will perform a non-destructive sync.")
            else:
                self.stdout.write(self.style.WARNING("No votes found. Wiping candidates and seats for clean load..."))
                Candidate.objects.all().delete()
                Seat.objects.all().delete()

        # Pre-fetch all seats for fast lookup
        seat_cache = {}
        for s in Seat.objects.all():
            key = (s.seat_type, s.county, s.constituency, s.ward)
            seat_cache[key] = s

        # Pre-fetch all candidates to avoid duplicates
        candidate_cache = {}
        for c in Candidate.objects.all():
            key = (c.seat_id, c.full_name.strip().lower())
            candidate_cache[key] = c

        candidates_to_create = []

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_rows = len(rows)
            self.stdout.write(f"Processing {total_rows} candidates...")

            for row_num, row in enumerate(rows, start=2):
                try:
                    full_name = row.get('full_name', '').strip()
                    party = row.get('party', '').strip()
                    seat_type = row.get('seat_type', '').strip()
                    level = row.get('level', '').strip()
                    
                    c_id = row.get('county_id', '').strip()
                    cn_id = row.get('constituency_id', '').strip()
                    w_id = row.get('ward_id', '').strip()

                    county_id = int(c_id) if c_id else None
                    constituency_id = int(cn_id) if cn_id else None
                    ward_id = int(w_id) if w_id else None

                    seat_key = (seat_type, county_id, constituency_id, ward_id)
                    
                    # 1. Ensure Seat exists
                    if seat_key not in seat_cache:
                        seat_name = f"{seat_type.title()} for {level}"
                        if level == 'National':
                            seat_name = f"{seat_type.title()} of Kenya"
                        elif level == 'County' and county_id:
                            from voting_api.views import KENYA_COUNTIES
                            seat_name = f"{seat_type.title()} for {KENYA_COUNTIES.get(county_id, f'County {county_id}')}"
                        
                        seat = Seat.objects.create(
                            seat_type=seat_type,
                            county=county_id,
                            constituency=constituency_id,
                            ward=ward_id,
                            level=level,
                            name=seat_name
                        )
                        seat_cache[seat_key] = seat
                    else:
                        seat = seat_cache[seat_key]

                    # 2. Check if candidate already exists in this seat
                    cand_key = (seat.id, full_name.lower())
                    if cand_key not in candidate_cache:
                        candidates_to_create.append(Candidate(
                            full_name=full_name,
                            party=party,
                            seat=seat
                        ))
                        # Add to cache to prevent duplicate in same file
                        candidate_cache[cand_key] = True 

                    if len(candidates_to_create) >= 2000:
                        Candidate.objects.bulk_create(candidates_to_create)
                        candidates_to_create = []
                        self.stdout.write(f"Buffered {row_num}/{total_rows}...")

                except Exception as e:
                    self.stderr.write(f"Error row {row_num}: {e}")

            # Final batch
            if candidates_to_create:
                # Filter out booleans from cache check
                actual_candidates = [c for c in candidates_to_create if not isinstance(c, bool)]
                Candidate.objects.bulk_create(actual_candidates)

        self.stdout.write(self.style.SUCCESS(f"Seeding completed. Total candidates: {Candidate.objects.count()}"))
