import os
import django
import sys
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

from voting_api.models import Candidate, Seat

FIRST_NAMES_M = ["John", "David", "Peter", "James", "Simon", "Joseph", "Daniel", "Michael", "Samuel", "Stephen", "Paul", "Kevin", "Brian", "Dennis", "Eric"]
FIRST_NAMES_F = ["Jane", "Mary", "Sarah", "Grace", "Faith", "Lucy", "Alice", "Mercy", "Joy", "Caroline", "Esther", "Lydia", "Ruth", "Gladys"]
PARTIES = ["UDA", "ODM", "Jubilee Party", "Wiper", "ANC", "Ford Kenya", "Safina", "KANU", "Independent"]

def get_surname_by_county(county_id):
    if county_id in [1, 2, 3, 4, 5, 6]:
        return random.choice(["Juma", "Bakari", "Ali", "Hassan", "Said", "Omar", "Salim", "Masha", "Nyale", "Badi"])
    elif county_id in [7, 8, 9, 10, 11]:
        return random.choice(["Abdi", "Farah", "Mohammed", "Ibrahim", "Yussuf", "Amina", "Fatuma", "Hussein", "Ahmed"])
    elif county_id in [12, 13, 14]:
        return random.choice(["Kinyua", "Njue", "Mugendi", "Mutegi", "Nyaga", "Kathomi", "Kawira"])
    elif county_id in [15, 16, 17]:
        return random.choice(["Mutua", "Mutiso", "Mwikali", "Kavila", "Wambua", "Musyoka", "Mutuku", "Mbithi"])
    elif county_id in [18, 19, 20, 21, 22]:
        return random.choice(["Kamau", "Njoroge", "Mwangi", "Ndung'u", "Maina", "Kariuki", "Njeri", "Wanjiku", "Wambui"])
    elif county_id in [23, 24, 25, 26]:
        return random.choice(["Ekal", "Lomuria", "Pkemoi", "Lempira", "Wanjala", "Khaemba", "Nasimiyu", "Ekitela"])
    elif county_id in [27, 28, 29, 30, 31, 32, 33, 34, 35, 36]:
        return random.choice(["Kipkorir", "Kiprotich", "Chebet", "Cheruiyot", "Kimutai", "Ruto", "Rono", "Ole Ntimama", "Letuya"])
    elif county_id in [37, 38, 39, 40]:
        return random.choice(["Wafula", "Wanjala", "Nekesa", "Nafula", "Shikuku", "Otsyula", "Ouma", "Wamalwa"])
    elif county_id in [41, 42, 43, 44]:
        return random.choice(["Ochieng", "Odhiambo", "Anyango", "Onyango", "Omondi", "Akinyi", "Awuor", "Otieno"])
    elif county_id in [45, 46]:
        return random.choice(["Makori", "Nyaboke", "Moraa", "Osoro", "Ombati", "Ongeri", "Mogaka", "Bosire"])
    else: # 47 Nairobi
        return random.choice(["Kamau", "Ochieng", "Wafula", "Kipkorir", "Mutua", "Juma", "Abdi", "Nyaboke"])

def generate_name(county_id):
    gender = random.choice(['M', 'F'])
    first = random.choice(FIRST_NAMES_M if gender == 'M' else FIRST_NAMES_F)
    surname = get_surname_by_county(county_id)
    return f"{first} {surname}"

print("Populating missing County level seats (Gov, Sen, Woman Rep)...")

for c_id in range(1, 48):
    # Governors
    gov_seat, _ = Seat.objects.get_or_create(seat_type='governor', level='County', county=c_id, defaults={'name': f"Governor for County {c_id}", 'icon': '🏛️'})
    if not Candidate.objects.filter(seat=gov_seat).exists():
        for _ in range(3):
            Candidate.objects.create(seat=gov_seat, full_name=generate_name(c_id), party=random.choice(PARTIES))

    # Senators
    sen_seat, _ = Seat.objects.get_or_create(seat_type='senator', level='County', county=c_id, defaults={'name': f"Senator for County {c_id}", 'icon': '⚖️'})
    if not Candidate.objects.filter(seat=sen_seat).exists():
        for _ in range(3):
            Candidate.objects.create(seat=sen_seat, full_name=generate_name(c_id), party=random.choice(PARTIES))

    # Women Rep
    wr_seat, _ = Seat.objects.get_or_create(seat_type='woman_rep', level='County', county=c_id, defaults={'name': f"Woman Rep for County {c_id}", 'icon': '👩'})
    if not Candidate.objects.filter(seat=wr_seat).exists():
        for _ in range(3):
            pf = random.choice(FIRST_NAMES_F)
            ps = get_surname_by_county(c_id)
            Candidate.objects.create(seat=wr_seat, full_name=f"{pf} {ps}", party=random.choice(PARTIES))

print("Fixed County successfully.")
