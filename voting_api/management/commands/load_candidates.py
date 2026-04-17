import csv
import os
from django.core.management.base import BaseCommand
from voting_api.models import Candidate, Seat

class Command(BaseCommand):
    help = 'Load candidates from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The absolute or relative path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File {csv_file} does not exist. Did you specify the right path?"))
            return

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            success_count = 0
            skip_count = 0
            
            for row_num, row in enumerate(reader, start=2):
                # ---------------------------------------------------------
                # THE TRY BLOCK
                # ---------------------------------------------------------
                try:
                    full_name = row.get('full_name', '').strip()
                    party = row.get('party', '').strip()
                    seat_type = row.get('seat_type', '').strip()
                    level = row.get('level', '').strip()
                    
                    county_id = row.get('county_id', '').strip()
                    constituency_id = row.get('constituency_id', '').strip()
                    ward_id = row.get('ward_id', '').strip()

                    # Convert string IDs back to Integers (or None if empty)
                    county_id = int(county_id) if county_id else None
                    constituency_id = int(constituency_id) if constituency_id else None
                    ward_id = int(ward_id) if ward_id else None

                    # If Seat doesn't exist, we will gracefully generate a dummy one to avoid crashing
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
                    
                    if created:
                        self.stdout.write(self.style.WARNING(f"Generated missing Seat dynamically: {seat}"))

                    # Create Candidate
                    Candidate.objects.create(
                        seat=seat,
                        full_name=full_name,
                        party=party
                    )
                    success_count += 1
                    
                # ---------------------------------------------------------
                # THE EXCEPT BLOCK - Catches the explosion
                # ---------------------------------------------------------
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Skipped Row {row_num} ({full_name}): {str(e)}"))
                    skip_count += 1
                    continue # Jump to the next row!

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {success_count} candidates. Skipped {skip_count} errors."))
