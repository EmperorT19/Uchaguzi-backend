from voting_api.models import Seat, Candidate

# Create Seats
president_seat, _ = Seat.objects.get_or_create(
    seat_type='president', level='National',
    defaults={'name': 'President of Kenya', 'icon': '🇰🇪'}
)

nakuru_governor, _ = Seat.objects.get_or_create(
    seat_type='governor', level='County', county='Nakuru',
    defaults={'name': 'Governor - Nakuru County', 'icon': '🏛️'}
)

nakuru_senator, _ = Seat.objects.get_or_create(
    seat_type='senator', level='County', county='Nakuru',
    defaults={'name': 'Senator - Nakuru County', 'icon': '⚖️'}
)

nakuru_womenrep, _ = Seat.objects.get_or_create(
    seat_type='woman_rep', level='County', county='Nakuru',
    defaults={'name': 'Woman Rep - Nakuru County', 'icon': '👩'}
)

naivasha_mp, _ = Seat.objects.get_or_create(
    seat_type='mp', level='Constituency', constituency='Naivasha',
    defaults={'name': 'MP - Naivasha', 'icon': '📋'}
)

maiella_mca, _ = Seat.objects.get_or_create(
    seat_type='mca', level='Ward', ward='Maiella',
    defaults={'name': 'MCA - Maiella Ward', 'icon': '🏘️'}
)

# Presidential Candidates (everyone sees these)
Candidate.objects.get_or_create(seat=president_seat, full_name='Dr. Jane Wanjiku Mwangi', defaults={'party': 'National Unity Alliance'})
Candidate.objects.get_or_create(seat=president_seat, full_name='Hon. David Kipchoge Korir', defaults={'party': 'Progressive Democratic Party'})
Candidate.objects.get_or_create(seat=president_seat, full_name='Prof. Grace Akinyi Otieno', defaults={'party': "People's Voice Movement"})

# Nakuru County candidates
Candidate.objects.get_or_create(seat=nakuru_governor, full_name='John Kamau Njoroge', defaults={'party': 'Jubilee Party'})
Candidate.objects.get_or_create(seat=nakuru_governor, full_name='Mary Wanjiru Kibet', defaults={'party': 'ODM'})

Candidate.objects.get_or_create(seat=nakuru_senator, full_name='Peter Ochieng Otieno', defaults={'party': 'Wiper'})
Candidate.objects.get_or_create(seat=nakuru_senator, full_name='Sarah Wambui Maina', defaults={'party': 'UDA'})

Candidate.objects.get_or_create(seat=nakuru_womenrep, full_name='Faith Muthoni Kariuki', defaults={'party': 'Jubilee Party'})
Candidate.objects.get_or_create(seat=nakuru_womenrep, full_name='Lucy Akinyi Odhiambo', defaults={'party': 'ODM'})

# Naivasha MP
Candidate.objects.get_or_create(seat=naivasha_mp, full_name='James Kiplagat Mutai', defaults={'party': 'UDA'})
Candidate.objects.get_or_create(seat=naivasha_mp, full_name='Rose Chebet Langat', defaults={'party': 'ANC'})

# Maiella MCA
Candidate.objects.get_or_create(seat=maiella_mca, full_name='David Mutua Kamau', defaults={'party': 'Jubilee Party'})
Candidate.objects.get_or_create(seat=maiella_mca, full_name='Jane Wanjiru Njau', defaults={'party': 'UDA'})

print("✅ Seed complete!")