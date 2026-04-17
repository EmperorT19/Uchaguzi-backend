import os
import django
import sys
import re
import random
from datetime import datetime

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_backend.settings')
django.setup()

from voting_api.models import Candidate, Seat

# 1. Parse REGISTRATION.TS for Locations
TS_PATH = r"c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-Frontend\src\app\components\registration\registration.ts"

print("Parsing registration.ts to extract geographic data...")
try:
    with open(TS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"ERROR: Could not find {TS_PATH}")
    sys.exit(1)

counties = []
constituencies = []
wards = []

# Regex to safely parse the nested JS array objects, even if slightly malformed
county_regex = re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*(?:'|\")([^'\"]+)(?:'|\")\s*\}", content.split('filteredConstituencies')[0])
for match in county_regex:
    counties.append({'id': int(match.group(1)), 'name': match.group(2)})

constit_text = content.split("wards = ")[0]
constit_regex = re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*(?:'|\")([^'\"]+)(?:'|\"),\s*countyId:\s*(\d+)\s*\}", constit_text)
for match in constit_regex:
    constituencies.append({
        'id': int(match.group(1)), 
        'name': match.group(2), 
        'countyId': int(match.group(3))
    })

ward_regex = re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*(?:'|\")([^'\"]+)(?:'|\"),\s*constituencyId:\s*(\d+)\s*\}", content)
for match in ward_regex:
    wards.append({
        'id': int(match.group(1)), 
        'name': match.group(2), 
        'constituencyId': int(match.group(3))
    })

print(f"Extracted: {len(counties)} Counties, {len(constituencies)} Constituencies, {len(wards)} Wards")

# 2. Candidate Generation Logic
FIRST_NAMES_M = ["John", "David", "Peter", "James", "Simon", "Joseph", "Daniel", "Michael", "Samuel", "Stephen", "Paul", "Kevin", "Brian", "Dennis", "Eric"]
FIRST_NAMES_F = ["Jane", "Mary", "Sarah", "Grace", "Faith", "Lucy", "Alice", "Mercy", "Joy", "Caroline", "Esther", "Lydia", "Ruth", "Gladys"]
PARTIES = ["UDA", "ODM", "Jubilee Party", "Wiper", "ANC", "Ford Kenya", "Safina", "KANU", "Independent"]

# Grouping Surnames by County IDs
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


print("\nClearing old database records...")
Candidate.objects.all().delete()
Seat.objects.all().delete()

print("Populating President...")
president_seat = Seat.objects.create(seat_type='president', level='National', name='President of Kenya', icon='🇰🇪')
for name, party in [('William Samoei Ruto', 'UDA'), ('Raila Amolo Odinga', 'Azimio'), ('George Wajackoyah', 'Roots Party'), ('David Mwaure Waihiga', 'Agano Party')]:
    Candidate.objects.create(seat=president_seat, full_name=name, party=party)


print("\nPopulating Governors, Senators, Women Reps (County Level)...")
for c in counties:
    # Governors
    gov_seat, _ = Seat.objects.get_or_create(seat_type='governor', level='County', county=c['id'], defaults={'name': f"{c['name']} Governor", 'icon': '🏛️'})
    for _ in range(3):
        Candidate.objects.create(seat=gov_seat, full_name=generate_name(c['id']), party=random.choice(PARTIES))

    # Senators
    sen_seat, _ = Seat.objects.get_or_create(seat_type='senator', level='County', county=c['id'], defaults={'name': f"{c['name']} Senator", 'icon': '⚖️'})
    for _ in range(3):
        Candidate.objects.create(seat=sen_seat, full_name=generate_name(c['id']), party=random.choice(PARTIES))

    # Women Rep
    wr_seat, _ = Seat.objects.get_or_create(seat_type='woman_rep', level='County', county=c['id'], defaults={'name': f"{c['name']} Woman Rep", 'icon': '👩'})
    for _ in range(3):
        pf = random.choice(FIRST_NAMES_F)
        ps = get_surname_by_county(c['id'])
        Candidate.objects.create(seat=wr_seat, full_name=f"{pf} {ps}", party=random.choice(PARTIES))


print("Populating MPs (Constituency Level)...")
# Map constituency to county for accurate regional names
const_county_map = { con['id']: con['countyId'] for con in constituencies }
for con in constituencies:
    mp_seat, _ = Seat.objects.get_or_create(
        seat_type='mp', level='Constituency', 
        county=con['countyId'], constituency=con['id'], 
        defaults={'name': f"MP - {con['name']}", 'icon': '📋'}
    )
    for _ in range(4):
        Candidate.objects.create(seat=mp_seat, full_name=generate_name(con['countyId']), party=random.choice(PARTIES))


print("Populating MCAs (Ward Level)...")
for w in wards:
    cid = w['constituencyId']
    county_id = const_county_map.get(cid, 47)  # Fallback to Nairobi if missing
    
    mca_seat, _ = Seat.objects.get_or_create(
        seat_type='mca', level='Ward', 
        county=county_id, constituency=cid, ward=w['id'], 
        defaults={'name': f"MCA - {w['name']}", 'icon': '🏘️'}
    )
    for _ in range(5):
        Candidate.objects.create(seat=mca_seat, full_name=generate_name(county_id), party=random.choice(PARTIES))

total_candidates = Candidate.objects.count()
print(f"\nSUCCESS! Generated and mapped exactly {total_candidates} candidates into the database.")
