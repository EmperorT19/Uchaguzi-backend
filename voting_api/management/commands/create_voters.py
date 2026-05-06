import random
import string
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from voting_api.models import Voter, Vote, Seat, Candidate

class Command(BaseCommand):
    help = 'Dynamically create users (voters) for a specific place and optionally mark them as having voted.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of voters to create')
        parser.add_argument('--county', type=str, required=True, help='County name for the voters')
        parser.add_argument('--constituency', type=str, required=True, help='Constituency name for the voters')
        parser.add_argument('--ward', type=str, required=True, help='Ward name for the voters')
        parser.add_argument('--voted', type=str, choices=['yes', 'no', 'random'], default='no', help='Whether these voters should have voted (yes/no/random)')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        county_name = kwargs['county']
        constituency_name = kwargs['constituency']
        ward_name = kwargs['ward']
        voted = kwargs['voted']

        # Look up IDs
        county_seat = Seat.objects.filter(level='County', name__icontains=county_name).first()
        const_seat = Seat.objects.filter(level='Constituency', name__icontains=constituency_name).first()
        ward_seat = Seat.objects.filter(level='Ward', name__icontains=ward_name).first()

        if not all([county_seat, const_seat, ward_seat]):
            self.stdout.write(self.style.ERROR("Could not find one or more of the specified regions. Check the spelling."))
            return

        county = county_seat.county
        constituency = const_seat.constituency
        ward = ward_seat.ward

        self.stdout.write(f"Found IDs - County: {county}, Constituency: {constituency}, Ward: {ward}")
        self.stdout.write(f"Creating {count} voters for County: {county_name}, Constituency: {constituency_name}, Ward: {ward_name}...")

        voters_created = []
        for i in range(count):
            random_id = ''.join(random.choices(string.digits, k=8))
            voter_code = f"V-{random_id}"
            
            voter = Voter.objects.create(
                voter_code=voter_code,
                full_name=f"Mock Voter {random_id}",
                id_number=random_id,
                phone_number=f"07{''.join(random.choices(string.digits, k=8))}",
                county=county,
                constituency=constituency,
                ward=ward,
                password_hash=make_password("Password123!")
            )
            voters_created.append(voter)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} voters."))

        if voted in ['yes', 'random']:
            # Find relevant seats
            seats = Seat.objects.filter(
                (Q(level='National')) |
                (Q(level='County', county=county)) |
                (Q(level='Constituency', county=county, constituency=constituency)) |
                (Q(level='Ward', county=county, constituency=constituency, ward=ward))
            )
            
            votes_to_create = []
            for voter in voters_created:
                # Determine if this specific voter votes
                if voted == 'random' and random.choice([True, False]) == False:
                    continue

                for seat in seats:
                    candidates = list(seat.candidates.all())
                    if candidates:
                        chosen_candidate = random.choice(candidates)
                        votes_to_create.append(Vote(
                            voter=voter,
                            seat=seat,
                            candidate=chosen_candidate
                        ))
            
            if votes_to_create:
                Vote.objects.bulk_create(votes_to_create)
                self.stdout.write(self.style.SUCCESS(f"Successfully cast {len(votes_to_create)} votes for the created users."))
            else:
                self.stdout.write(self.style.WARNING("No votes were cast. Ensure candidates exist for the specified region."))
