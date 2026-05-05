import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

from voting_api.models import Seat

county = Seat.objects.filter(level='County', name__icontains='Mombasa').first()
if county:
    print(f"County Mombasa ID: {county.county}")

const = Seat.objects.filter(level='Constituency', name__icontains='Mvita').first()
if const:
    print(f"Constituency Mvita ID: {const.constituency}")

ward = Seat.objects.filter(level='Ward', name__icontains='Tudor').first()
if ward:
    print(f"Ward Tudor ID: {ward.ward}")
