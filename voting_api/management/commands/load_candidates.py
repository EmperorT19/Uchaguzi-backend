# Optimized Candidate Seeding Script: 
# Uses bulk_create to import ~15,000 regional candidates without database timeouts.
import csv
import os
from django.core.management.base import BaseCommand
from voting_api.models import Candidate, Seat

class Command(BaseCommand):
    help = 'Load candidates from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The absolute or relative path to the CSV file')
        parser.add_argument('--force', action='store_true', help='Force wipe and load')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if kwargs.get('force'):
            self.stdout.write(self.style.WARNING("Force flag passed. Wiping old data..."))
            Candidate.objects.all().delete()
            # Also clear seats except maybe we don't want to break foreign keys of Votes?
            # Wait! If we delete Candidate, Votes to that candidate are CASCADE deleted. 
            # If we delete Seat, Votes to that seat are CASCADE deleted. 
            # This is an emergency wipe, we have to recreate them.
            Seat.objects.all().delete()
        else:
            existing = Candidate.objects.count()
            if existing > 0:
                self.stdout.write(self.style.SUCCESS(
                    f"Database already has {existing} candidates. Skipping load."
                ))
                return

        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File {csv_file} does not exist. Did you specify the right path?"))
            return

        # Cache for seats to avoid redundant DB queries
        seat_cache = {}
        for s in Seat.objects.all():
            key = (s.seat_type, s.county, s.constituency, s.ward)
            seat_cache[key] = s

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            candidates_to_create = []
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    full_name = row.get('full_name', '').strip()
                    party = row.get('party', '').strip()
                    seat_type = row.get('seat_type', '').strip()
                    level = row.get('level', '').strip()
                    
                    county_id = row.get('county_id', '').strip()
                    constituency_id = row.get('constituency_id', '').strip()
                    ward_id = row.get('ward_id', '').strip()

                    county_id = int(county_id) if county_id else None
                    constituency_id = int(constituency_id) if constituency_id else None
                    ward_id = int(ward_id) if ward_id else None

                    seat_key = (seat_type, county_id, constituency_id, ward_id)
                    
                    if seat_key not in seat_cache:
                        seat, created = Seat.objects.get_or_create(
                            seat_type=seat_type,
                            county=county_id,
                            constituency=constituency_id,
                            ward=ward_id,
                            defaults={
                                'level': level,
                                'name': f"{seat_type.title()} {level}"
                            }
                        )
                        seat_cache[seat_key] = seat
                        if created:
                            self.stdout.write(self.style.WARNING(f"Generated missing Seat dynamically: {seat}"))
                    
                    seat = seat_cache[seat_key]

                    candidates_to_create.append(Candidate(
                        seat=seat,
                        full_name=full_name,
                        party=party
                    ))
                    
                    if len(candidates_to_create) >= 1000:
                        Candidate.objects.bulk_create(candidates_to_create)
                        candidates_to_create = []
                    
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Skipped Row {row_num}: {str(e)}"))
                    continue

            if candidates_to_create:
                Candidate.objects.bulk_create(candidates_to_create)

        total_final = Candidate.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Successfully synchronized candidates. Total in DB: {total_final}"))
