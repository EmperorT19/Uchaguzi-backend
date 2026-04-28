import uuid
import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
from.models import *
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt

# ============================================================
# Paste WARD_LOOKUP and get_candidates into views.py
# ward_id -> (ward_name, constituency_name, county_name)
# Built from the Angular registration data — all 1448 wards
# ============================================================

# WARD_LOOKUP = {
#     1: ('Port Reitz', 'Changamwe', 'Mombasa'),
#     2: ('Kipevu', 'Changamwe', 'Mombasa'),
#     3: ('Airport', 'Changamwe', 'Mombasa'),
#     4: ('Miritini', 'Changamwe', 'Mombasa'),
#     5: ('Chaani', 'Changamwe', 'Mombasa'),
#     6: ('Jomvu Kuu', 'Jomvu', 'Mombasa'),
#     7: ('Magongo', 'Jomvu', 'Mombasa'),
#     8: ('Mikindani', 'Jomvu', 'Mombasa'),
#     9: ('Mjambere', 'Kisauni', 'Mombasa'),
#     10: ('Junda', 'Kisauni', 'Mombasa'),
#     11: ('Bamburi', 'Kisauni', 'Mombasa'),
#     12: ('Mwakirunge', 'Kisauni', 'Mombasa'),
#     13: ('Mtopanga', 'Kisauni', 'Mombasa'),
#     14: ('Magogoni', 'Kisauni', 'Mombasa'),
#     15: ('Shanzu', 'Kisauni', 'Mombasa'),
#     16: ('Mtongwe', 'Nyali', 'Mombasa'),
#     17: ('Shika adabu', 'Nyali', 'Mombasa'),
#     18: ('Bofu', 'Nyali', 'Mombasa'),
#     19: ('Likoni', 'Nyali', 'Mombasa'),
#     20: ('Timbwani', 'Nyali', 'Mombasa'),
#     21: ('Mji wa Kale/Makadara', 'Likoni', 'Mombasa'),
#     22: ('Tudor', 'Likoni', 'Mombasa'),
#     23: ('Tononoka', 'Likoni', 'Mombasa'),
#     24: ('Ganjoni/Shimanzi', 'Likoni', 'Mombasa'),
#     25: ('Majengo', 'Likoni', 'Mombasa'),
#     26: ('Frere Town', 'Mvita', 'Mombasa'),
#     27: ("Ziwa la Ng'ombe", 'Mvita', 'Mombasa'),
#     28: ('Mkomani', 'Mvita', 'Mombasa'),
#     29: ('Kongowea', 'Mvita', 'Mombasa'),
#     30: ('Ziwani/Kadzandani', 'Mvita', 'Mombasa'),
#     31: ('Ndavaya', 'Msambweni', 'Kwale'),
#     32: ('Puma', 'Msambweni', 'Kwale'),
#     33: ('Kinango', 'Msambweni', 'Kwale'),
#     34: ('Chengoni/Samburu', 'Msambweni', 'Kwale'),
#     35: ('Mackinon Road', 'Msambweni', 'Kwale'),
#     36: ('Mwavumbo', 'Msambweni', 'Kwale'),
#     37: ('Kasemeni', 'Msambweni', 'Kwale'),
#     38: ('Pongwe/Kikoneni', 'Lunga Lunga', 'Kwale'),
#     39: ('Dzombo', 'Lunga Lunga', 'Kwale'),
#     40: ('Vanga', 'Lunga Lunga', 'Kwale'),
#     41: ('Mwereni', 'Lunga Lunga', 'Kwale'),
#     42: ('Gombato Bongwe', 'Matuga', 'Kwale'),
#     43: ('Ukunda', 'Matuga', 'Kwale'),
#     44: ('Kinondo', 'Matuga', 'Kwale'),
#     45: ('Ramisi', 'Matuga', 'Kwale'),
#     46: ('Tsimba Golini', 'Kinango', 'Kwale'),
#     47: ('Waa', 'Kinango', 'Kwale'),
#     48: ('Tiwi', 'Kinango', 'Kwale'),
#     49: ('Kubo South', 'Kinango', 'Kwale'),
#     50: ('Mkongani', 'Kinango', 'Kwale'),
#     51: ('Tezo', 'Kilifi North', 'Kilifi'),
#     52: ('Sokoni', 'Kilifi North', 'Kilifi'),
#     53: ('Kibarani', 'Kilifi North', 'Kilifi'),
#     54: ('Dabaso', 'Kilifi North', 'Kilifi'),
#     55: ('Matsangoni', 'Kilifi North', 'Kilifi'),
#     56: ('Watamu', 'Kilifi North', 'Kilifi'),
#     57: ('Mnarani', 'Kilifi North', 'Kilifi'),
#     58: ('Junju', 'Kilifi South', 'Kilifi'),
#     59: ('Mwarakaya', 'Kilifi South', 'Kilifi'),
#     60: ('Shimo la Tewa', 'Kilifi South', 'Kilifi'),
#     61: ('Chasimba', 'Kilifi South', 'Kilifi'),
#     62: ('Mtepeni', 'Kilifi South', 'Kilifi'),
#     63: ('Mariakani', 'Kaloleni', 'Kilifi'),
#     64: ('Kayafungo', 'Kaloleni', 'Kilifi'),
#     65: ('Kaloleni', 'Kaloleni', 'Kilifi'),
#     66: ('Mwanamwinga', 'Kaloleni', 'Kilifi'),
#     67: ('Dungicha', 'Rabai', 'Kilifi'),
#     68: ('Bamba', 'Rabai', 'Kilifi'),
#     69: ('Jaribuni', 'Rabai', 'Kilifi'),
#     70: ('Sokoke', 'Rabai', 'Kilifi'),
#     71: ('Maarafa', 'Ganze', 'Kilifi'),
#     72: ('Magarini', 'Ganze', 'Kilifi'),
#     73: ('Gongoni', 'Ganze', 'Kilifi'),
#     74: ('Adu', 'Ganze', 'Kilifi'),
#     75: ('Garashi', 'Ganze', 'Kilifi'),
#     76: ('Sabaki', 'Ganze', 'Kilifi'),
#     77: ('Mwawesa', 'Malindi', 'Kilifi'),
#     78: ('Ruruma', 'Malindi', 'Kilifi'),
#     79: ('Jibana', 'Malindi', 'Kilifi'),
#     80: ('Rabai/Kisurutuni', 'Malindi', 'Kilifi'),
#     81: ('Jilore', 'Magarini', 'Kilifi'),
#     82: ('Kakuyuni', 'Magarini', 'Kilifi'),
#     83: ('Ganda', 'Magarini', 'Kilifi'),
#     84: ('Malindi Town', 'Magarini', 'Kilifi'),
#     85: ('Shella', 'Magarini', 'Kilifi'),
#     86: ('Garsen Central', 'Garsen', 'Tana River'),
#     87: ('Garsen East', 'Garsen', 'Tana River'),
#     88: ('Garsen North', 'Garsen', 'Tana River'),
#     89: ('Garsen South', 'Garsen', 'Tana River'),
#     90: ('Kipini East', 'Garsen', 'Tana River'),
#     91: ('Kipini West', 'Garsen', 'Tana River'),
#     92: ('Kinakomba', 'Galole', 'Tana River'),
#     93: ('Mikinduni', 'Galole', 'Tana River'),
#     94: ('Chewani', 'Galole', 'Tana River'),
#     95: ('Wayu', 'Galole', 'Tana River'),
#     96: ('Chewele', 'Bura', 'Tana River'),
#     97: ('Hirimani', 'Bura', 'Tana River'),
#     98: ('Bangale', 'Bura', 'Tana River'),
#     99: ('Madogo', 'Bura', 'Tana River'),
#     100: ('Sala', 'Bura', 'Tana River'),
#     101: ('Faza', 'Lamu East', 'Lamu'),
#     102: ('Kiunga', 'Lamu East', 'Lamu'),
#     103: ('Basuba', 'Lamu East', 'Lamu'),
#     104: ('Shella', 'Lamu West', 'Lamu'),
#     105: ('Mkomani', 'Lamu West', 'Lamu'),
#     106: ('Hindi', 'Lamu West', 'Lamu'),
#     107: ('Mkunumbi', 'Lamu West', 'Lamu'),
#     108: ('Hongwe', 'Lamu West', 'Lamu'),
#     109: ('Witu', 'Lamu West', 'Lamu'),
#     110: ('Bahari', 'Lamu West', 'Lamu'),
#     111: ('Chala', 'Taveta', 'Taita-Taveta'),
#     112: ('Mahoo', 'Taveta', 'Taita-Taveta'),
#     113: ('Bomani', 'Taveta', 'Taita-Taveta'),
#     114: ('Mboghoni', 'Taveta', 'Taita-Taveta'),
#     115: ('Mata', 'Taveta', 'Taita-Taveta'),
#     116: ('Wundanyi/Mbale', 'Wundanyi', 'Taita-Taveta'),
#     117: ('Werugha', 'Wundanyi', 'Taita-Taveta'),
#     118: ('Wumingu/Kishushe', 'Wundanyi', 'Taita-Taveta'),
#     119: ('Mwanda/Mgange', 'Wundanyi', 'Taita-Taveta'),
#     120: ('Ronge', 'Mwatate', 'Taita-Taveta'),
#     121: ('Mwatate', 'Mwatate', 'Taita-Taveta'),
#     122: ('Bura', 'Mwatate', 'Taita-Taveta'),
#     123: ('Chawia', 'Mwatate', 'Taita-Taveta'),
#     124: ('Wusi/Kishamba', 'Mwatate', 'Taita-Taveta'),
#     125: ('Mbololo', 'Voi', 'Taita-Taveta'),
#     126: ('Kaloleni', 'Voi', 'Taita-Taveta'),
#     127: ('Sagala', 'Voi', 'Taita-Taveta'),
#     128: ('Marungu', 'Voi', 'Taita-Taveta'),
#     129: ('Kaigau', 'Voi', 'Taita-Taveta'),
#     130: ('Ngolia', 'Voi', 'Taita-Taveta'),
#     131: ('Waberi', 'Garissa Township', 'Garissa'),
#     132: ('Galbet', 'Garissa Township', 'Garissa'),
#     133: ('Township', 'Garissa Township', 'Garissa'),
#     134: ('Iftin', 'Garissa Township', 'Garissa'),
#     135: ('Balambala', 'Balambala', 'Garissa'),
#     136: ('Danyere', 'Balambala', 'Garissa'),
#     137: ('Jarajara', 'Balambala', 'Garissa'),
#     138: ('Saka', 'Balambala', 'Garissa'),
#     139: ('Sankuri', 'Balambala', 'Garissa'),
#     140: ('Dertu', 'Lagdera', 'Garissa'),
#     141: ('Dadaab', 'Lagdera', 'Garissa'),
#     142: ('Labasigale', 'Lagdera', 'Garissa'),
#     143: ('Damajale', 'Lagdera', 'Garissa'),
#     144: ('Liboi', 'Lagdera', 'Garissa'),
#     145: ('Abakaile', 'Lagdera', 'Garissa'),
#     146: ('Bura', 'Dadaab', 'Garissa'),
#     147: ('Dekaharia', 'Dadaab', 'Garissa'),
#     148: ('Jarajila', 'Dadaab', 'Garissa'),
#     149: ('Fafi', 'Dadaab', 'Garissa'),
#     150: ('Nanighi', 'Dadaab', 'Garissa'),
#     151: ('Hulugho', 'Fafi', 'Garissa'),
#     152: ('Sangailu', 'Fafi', 'Garissa'),
#     153: ('Ijara', 'Fafi', 'Garissa'),
#     154: ('Masalani', 'Fafi', 'Garissa'),
#     155: ('Modogashe', 'Ijara', 'Garissa'),
#     156: ('Bename', 'Ijara', 'Garissa'),
#     157: ('Goreale', 'Ijara', 'Garissa'),
#     158: ('Maalamin', 'Ijara', 'Garissa'),
#     159: ('Sabena', 'Ijara', 'Garissa'),
#     160: ('Baraki', 'Ijara', 'Garissa'),
#     161: ('Wagbri', 'Wajir North', 'Wajir'),
#     162: ('Township', 'Wajir North', 'Wajir'),
#     163: ('Barwago', 'Wajir North', 'Wajir'),
#     164: ('Khorof/Harar', 'Wajir North', 'Wajir'),
#     165: ('Gurar', 'Wajir East', 'Wajir'),
#     166: ('Bute', 'Wajir East', 'Wajir'),
#     167: ('Korondile', 'Wajir East', 'Wajir'),
#     168: ('Malkagufu', 'Wajir East', 'Wajir'),
#     169: ('Batalu', 'Wajir East', 'Wajir'),
#     170: ('Danaba', 'Wajir East', 'Wajir'),
#     171: ('Godoma', 'Wajir East', 'Wajir'),
#     172: ('Benane', 'Tarbaj', 'Wajir'),
#     173: ('Burder', 'Tarbaj', 'Wajir'),
#     174: ('Dadaja Bulla', 'Tarbaj', 'Wajir'),
#     175: ('Habaswein', 'Tarbaj', 'Wajir'),
#     176: ('Lagboghol South', 'Tarbaj', 'Wajir'),
#     177: ('Ibrahim Ure', 'Tarbaj', 'Wajir'),
#     178: ('Arbajahan', 'Wajir West', 'Wajir'),
#     179: ('Hadado/Athibohol', 'Wajir West', 'Wajir'),
#     180: ('Ademasajide', 'Wajir West', 'Wajir'),
#     181: ('Ganyure', 'Wajir West', 'Wajir'),
#     182: ('Wagalla', 'Wajir West', 'Wajir'),
#     183: ('Elben', 'Eldas', 'Wajir'),
#     184: ('Sarman', 'Eldas', 'Wajir'),
#     185: ('Tarbaj', 'Eldas', 'Wajir'),
#     186: ('Wargadud', 'Eldas', 'Wajir'),
#     187: ('Eldas', 'Wajir South', 'Wajir'),
#     188: ('Della', 'Wajir South', 'Wajir'),
#     189: ('Lakoley South/Basir', 'Wajir South', 'Wajir'),
#     190: ('Elnur/Tula Tula', 'Wajir South', 'Wajir'),
#     191: ('Takaba South', 'Mandera West', 'Mandera'),
#     192: ('Takaba', 'Mandera West', 'Mandera'),
#     193: ('Lagsure', 'Mandera West', 'Mandera'),
#     194: ('Dandu', 'Mandera West', 'Mandera'),
#     195: ('Gither', 'Mandera West', 'Mandera'),
#     196: ('Banissa', 'Banissa', 'Mandera'),
#     197: ('Derkhale', 'Banissa', 'Mandera'),
#     198: ('Guba', 'Banissa', 'Mandera'),
#     199: ('Malkamari', 'Banissa', 'Mandera'),
#     200: ('Kiliwehiri', 'Banissa', 'Mandera'),
#     201: ('Ashabito', 'Mandera North', 'Mandera'),
#     202: ('Guticha', 'Mandera North', 'Mandera'),
#     203: ('Marothile', 'Mandera North', 'Mandera'),
#     204: ('Rhamu', 'Mandera North', 'Mandera'),
#     205: ('Rhamu Dimtu', 'Mandera North', 'Mandera'),
#     206: ('Wargadud', 'Mandera South', 'Mandera'),
#     207: ('Kutulo', 'Mandera South', 'Mandera'),
#     208: ('Elwak South', 'Mandera South', 'Mandera'),
#     209: ('Elwak North', 'Mandera South', 'Mandera'),
#     210: ('Shimbir Fatuma', 'Mandera South', 'Mandera'),
#     211: ('Arabia', 'Mandera East', 'Mandera'),
#     212: ('Libehia', 'Mandera East', 'Mandera'),
#     213: ('Khalalio', 'Mandera East', 'Mandera'),
#     214: ('Neboi', 'Mandera East', 'Mandera'),
#     215: ('Township', 'Mandera East', 'Mandera'),
#     216: ('Sala', 'Lafey', 'Mandera'),
#     217: ('Fino', 'Lafey', 'Mandera'),
#     218: ('Lafey', 'Lafey', 'Mandera'),
#     219: ('Warangara', 'Lafey', 'Mandera'),
#     220: ('Alungo', 'Lafey', 'Mandera'),
#     221: ('Loiyangalani', 'Moyale', 'Marsabit'),
#     222: ('Kargi/South Horr', 'Moyale', 'Marsabit'),
#     223: ('Korr/Ngurunit', 'Moyale', 'Marsabit'),
#     224: ('LogoLogo', 'Moyale', 'Marsabit'),
#     225: ('Laisamis', 'Moyale', 'Marsabit'),
#     226: ('Dukana', 'North Horr', 'Marsabit'),
#     227: ('Maikona', 'North Horr', 'Marsabit'),
#     228: ('Turbi', 'North Horr', 'Marsabit'),
#     229: ('North Horr', 'North Horr', 'Marsabit'),
#     230: ('Illeret', 'North Horr', 'Marsabit'),
#     231: ('Sagate/Jaldesa', 'Saku', 'Marsabit'),
#     232: ('Karare', 'Saku', 'Marsabit'),
#     233: ('Marsabit Central', 'Saku', 'Marsabit'),
#     234: ('Butiye', 'Laisamis', 'Marsabit'),
#     235: ('Sololo', 'Laisamis', 'Marsabit'),
#     236: ('Heillu/Manyatta', 'Laisamis', 'Marsabit'),
#     237: ('Golbo', 'Laisamis', 'Marsabit'),
#     238: ('Moyale Township', 'Laisamis', 'Marsabit'),
#     239: ('Uran', 'Laisamis', 'Marsabit'),
#     240: ('Obbu', 'Laisamis', 'Marsabit'),
#     241: ('Wabera', 'Isiolo North', 'Isiolo'),
#     242: ('Bulla Pesa', 'Isiolo North', 'Isiolo'),
#     243: ('Chari', 'Isiolo North', 'Isiolo'),
#     244: ('Cherab', 'Isiolo North', 'Isiolo'),
#     245: ('Ngare Mara', 'Isiolo North', 'Isiolo'),
#     246: ('Burat', 'Isiolo North', 'Isiolo'),
#     247: ('Oldo/Nyiro', 'Isiolo North', 'Isiolo'),
#     248: ('Garba Tulla', 'Isiolo South', 'Isiolo'),
#     249: ('Kina', 'Isiolo South', 'Isiolo'),
#     250: ('Sericho', 'Isiolo South', 'Isiolo'),
#     251: ('Timau', 'Igembe South', 'Meru'),
#     252: ('Kisima', 'Igembe South', 'Meru'),
#     253: ('Kiirua/Naari', 'Igembe South', 'Meru'),
#     254: ('Ruiri/Rwarera', 'Igembe South', 'Meru'),
#     255: ('Mwanganthia', 'Igembe Central', 'Meru'),
#     256: ('Abothuguchi Central', 'Igembe Central', 'Meru'),
#     257: ('Abothuguchi West', 'Igembe Central', 'Meru'),
#     258: ('Kiagu', 'Igembe Central', 'Meru'),
#     259: ('Kibirichia', 'Igembe Central', 'Meru'),
#     260: ("Akirang'ondu", 'Igembe North', 'Meru'),
#     261: ('Athiru', 'Igembe North', 'Meru'),
#     262: ('Ruujine', 'Igembe North', 'Meru'),
#     263: ('Igembe East Njia', 'Igembe North', 'Meru'),
#     264: ('Kangeta', 'Igembe North', 'Meru'),
#     265: ('Maua', 'Tigania West', 'Meru'),
#     266: ('Kegoi/Antubochiu', 'Tigania West', 'Meru'),
#     267: ('Athiru', 'Tigania West', 'Meru'),
#     268: ('Gaiti', 'Tigania West', 'Meru'),
#     269: ('Akachiu', 'Tigania West', 'Meru'),
#     270: ('Kanuni', 'Tigania West', 'Meru'),
#     271: ('Antuambui', 'Tigania East', 'Meru'),
#     272: ('Ntunene', 'Tigania East', 'Meru'),
#     273: ('Antubetwe Kiongo', 'Tigania East', 'Meru'),
#     274: ('Naathui', 'Tigania East', 'Meru'),
#     275: ('Amwathi', 'Tigania East', 'Meru'),
#     276: ('Athwana', 'North Imenti', 'Meru'),
#     277: ('Akithi', 'North Imenti', 'Meru'),
#     278: ('Kianjai', 'North Imenti', 'Meru'),
#     279: ('Nkomo', 'North Imenti', 'Meru'),
#     280: ('Mbeu', 'North Imenti', 'Meru'),
#     281: ('Thangatha', 'Buuri', 'Meru'),
#     282: ('Mikinduri', 'Buuri', 'Meru'),
#     283: ('Kiguchwa', 'Buuri', 'Meru'),
#     284: ('Mithara', 'Buuri', 'Meru'),
#     285: ('Karama', 'Buuri', 'Meru'),
#     286: ('Municipality', 'Central Imenti', 'Meru'),
#     287: ('Ntima East', 'Central Imenti', 'Meru'),
#     288: ('Ntima West', 'Central Imenti', 'Meru'),
#     289: ('Nyaki West', 'Central Imenti', 'Meru'),
#     290: ('Nyaki East', 'Central Imenti', 'Meru'),
#     291: ('Mitunguu', 'South Imenti', 'Meru'),
#     292: ('Igoji East', 'South Imenti', 'Meru'),
#     293: ('Igoji West', 'South Imenti', 'Meru'),
#     294: ('Abogeta East', 'South Imenti', 'Meru'),
#     295: ('Abogeta West', 'South Imenti', 'Meru'),
#     296: ('Nkuene', 'South Imenti', 'Meru'),
#     297: ('Gatunga', 'Maara', 'Tharaka-Nithi'),
#     298: ('Mukothima', 'Maara', 'Tharaka-Nithi'),
#     299: ('Nkondi', 'Maara', 'Tharaka-Nithi'),
#     300: ('Chiakariga', 'Maara', 'Tharaka-Nithi'),
#     301: ('Marimanti', 'Maara', 'Tharaka-Nithi'),
#     302: ('Mariani', "Chuka/Igambang'ombe", 'Tharaka-Nithi'),
#     303: ('Karingani', "Chuka/Igambang'ombe", 'Tharaka-Nithi'),
#     304: ('Magumoni', "Chuka/Igambang'ombe", 'Tharaka-Nithi'),
#     305: ('Mugwe', "Chuka/Igambang'ombe", 'Tharaka-Nithi'),
#     306: ("Igambang'ombe", "Chuka/Igambang'ombe", 'Tharaka-Nithi'),
#     307: ('Mitheru', 'Tharaka', 'Tharaka-Nithi'),
#     308: ('Muthambi', 'Tharaka', 'Tharaka-Nithi'),
#     309: ('Mwimbi', 'Tharaka', 'Tharaka-Nithi'),
#     310: ('Ganga', 'Tharaka', 'Tharaka-Nithi'),
#     311: ('Chogoria', 'Tharaka', 'Tharaka-Nithi'),
#     312: ('Ruguru/Ngandori', 'Manyatta', 'Embu'),
#     313: ('Kithimu', 'Manyatta', 'Embu'),
#     314: ('Nginda', 'Manyatta', 'Embu'),
#     315: ('Mbeti North', 'Manyatta', 'Embu'),
#     316: ('Kirimari', 'Manyatta', 'Embu'),
#     317: ('Gaturi South', 'Manyatta', 'Embu'),
#     318: ('Gaturi North', 'Runyenjes', 'Embu'),
#     319: ('Kagaari South', 'Runyenjes', 'Embu'),
#     320: ('Kagaari North', 'Runyenjes', 'Embu'),
#     321: ('Central Ward', 'Runyenjes', 'Embu'),
#     322: ('Kyeni North', 'Runyenjes', 'Embu'),
#     323: ('Kyeni South', 'Runyenjes', 'Embu'),
#     324: ('Nthawa', 'Mbeere South', 'Embu'),
#     325: ('Muminji', 'Mbeere South', 'Embu'),
#     326: ('Evurore', 'Mbeere South', 'Embu'),
#     327: ('Mwea', 'Mbeere North', 'Embu'),
#     328: ('Amakim', 'Mbeere North', 'Embu'),
#     329: ('Mbeti South', 'Mbeere North', 'Embu'),
#     330: ('Mavuria', 'Mbeere North', 'Embu'),
#     331: ('Kiambere', 'Mbeere North', 'Embu'),
#     332: ('Mutonguni', 'Mwingi North', 'Kitui'),
#     333: ('Kauwi', 'Mwingi North', 'Kitui'),
#     334: ('Matinyani', 'Mwingi North', 'Kitui'),
#     335: ('Kwa Mutonga/Kithum Ula', 'Mwingi North', 'Kitui'),
#     336: ('Miambani', 'Mwingi West', 'Kitui'),
#     337: ('Township Kyangwithya West', 'Mwingi West', 'Kitui'),
#     338: ('Mulango', 'Mwingi West', 'Kitui'),
#     339: ('Kyangwithya East', 'Mwingi West', 'Kitui'),
#     340: ('Kisasi', 'Mwingi Central', 'Kitui'),
#     341: ('Mbitini', 'Mwingi Central', 'Kitui'),
#     342: ('Kwavonza/Yatta', 'Mwingi Central', 'Kitui'),
#     343: ('Kanyangi', 'Mwingi Central', 'Kitui'),
#     344: ('Ikana/Kyantune', 'Kitui West', 'Kitui'),
#     345: ('Mutomo', 'Kitui West', 'Kitui'),
#     346: ('Mutha', 'Kitui West', 'Kitui'),
#     347: ('Ikutha', 'Kitui West', 'Kitui'),
#     348: ('Kanziko', 'Kitui West', 'Kitui'),
#     349: ('Athi', 'Kitui West', 'Kitui'),
#     350: ('Zombe/Mwitika', 'Kitui Rural', 'Kitui'),
#     351: ('Nzambani', 'Kitui Rural', 'Kitui'),
#     352: ('Chuluni', 'Kitui Rural', 'Kitui'),
#     353: ('Voo/Kyamatu', 'Kitui Rural', 'Kitui'),
#     354: ('Endau/Malalani', 'Kitui Rural', 'Kitui'),
#     355: ('Mutito/Kaliku', 'Kitui Rural', 'Kitui'),
#     356: ('Ngomeni', 'Kitui Central', 'Kitui'),
#     357: ('Kyuso', 'Kitui Central', 'Kitui'),
#     358: ('Mumoni', 'Kitui Central', 'Kitui'),
#     359: ('Tseikuru', 'Kitui Central', 'Kitui'),
#     360: ('Tharaka', 'Kitui Central', 'Kitui'),
#     361: ('Kyome/Thaana', 'Kitui East', 'Kitui'),
#     362: ('Nguutani', 'Kitui East', 'Kitui'),
#     363: ('Migwani', 'Kitui East', 'Kitui'),
#     364: ('Kiomo/Kyethani', 'Kitui East', 'Kitui'),
#     365: ('Central', 'Kitui South', 'Kitui'),
#     366: ('Kivou', 'Kitui South', 'Kitui'),
#     367: ('Nguni', 'Kitui South', 'Kitui'),
#     368: ('Mui', 'Kitui South', 'Kitui'),
#     369: ('Waita', 'Kitui South', 'Kitui'),
#     370: ('Kivaa', 'Masinga', 'Machakos'),
#     371: ('Masinga', 'Masinga', 'Machakos'),
#     372: ('Central', 'Masinga', 'Machakos'),
#     373: ('Ekalakala', 'Masinga', 'Machakos'),
#     374: ('Muthesya', 'Masinga', 'Machakos'),
#     375: ('Ndithini', 'Masinga', 'Machakos'),
#     376: ('Ndalani', 'Yatta', 'Machakos'),
#     377: ('Matuu', 'Yatta', 'Machakos'),
#     378: ('Kithimani', 'Yatta', 'Machakos'),
#     379: ('Ikomba', 'Yatta', 'Machakos'),
#     380: ('Katangi', 'Yatta', 'Machakos'),
#     381: ('Tala', 'Kangundo', 'Machakos'),
#     382: ('Matungulu North', 'Kangundo', 'Machakos'),
#     383: ('Matungulu East', 'Kangundo', 'Machakos'),
#     384: ('Matungulu West', 'Kangundo', 'Machakos'),
#     385: ('Kyeleni', 'Kangundo', 'Machakos'),
#     386: ('Kangundo North', 'Matungulu', 'Machakos'),
#     387: ('Kangundo Central', 'Matungulu', 'Machakos'),
#     388: ('Kangundo East', 'Matungulu', 'Machakos'),
#     389: ('Kangundo West', 'Matungulu', 'Machakos'),
#     390: ('Mbiuni', 'Kathiani', 'Machakos'),
#     391: ('Makutano/Mwala', 'Kathiani', 'Machakos'),
#     392: ('Masii', 'Kathiani', 'Machakos'),
#     393: ('Muthetheni', 'Kathiani', 'Machakos'),
#     394: ('Wamunyu', 'Kathiani', 'Machakos'),
#     395: ('Kibauni', 'Kathiani', 'Machakos'),
#     396: ('Mitaboni', 'Mavoko', 'Machakos'),
#     397: ('Kathiani Central', 'Mavoko', 'Machakos'),
#     398: ('Upper Kaewa/Iveti', 'Mavoko', 'Machakos'),
#     399: ('Lower Kaewa/Kaani', 'Mavoko', 'Machakos'),
#     400: ('Kalama', 'Machakos Town', 'Machakos'),
#     401: ('Mua', 'Machakos Town', 'Machakos'),
#     402: ('Mutitini', 'Machakos Town', 'Machakos'),
#     403: ('Machakos Central', 'Machakos Town', 'Machakos'),
#     404: ('Mumbuni North', 'Machakos Town', 'Machakos'),
#     405: ('Muvuti/Kiima-Kimwe', 'Machakos Town', 'Machakos'),
#     406: ('Kola', 'Machakos Town', 'Machakos'),
#     407: ('Athi River', 'Mwala', 'Machakos'),
#     408: ('Kinanie', 'Mwala', 'Machakos'),
#     409: ('Muthwani', 'Mwala', 'Machakos'),
#     410: ('Syokimau/Mulolongo', 'Mwala', 'Machakos'),
#     411: ('Tulimani', 'Mbooni', 'Makueni'),
#     412: ('Mbooni', 'Mbooni', 'Makueni'),
#     413: ('Kithungo/Kitundu', 'Mbooni', 'Makueni'),
#     414: ('Kiteta/Kisau', 'Mbooni', 'Makueni'),
#     415: ('Waia-Kako', 'Mbooni', 'Makueni'),
#     416: ('Kalawa', 'Mbooni', 'Makueni'),
#     417: ('Ukia', 'Kilome', 'Makueni'),
#     418: ('Kee', 'Kilome', 'Makueni'),
#     419: ('Kilungu', 'Kilome', 'Makueni'),
#     420: ('Ilima', 'Kilome', 'Makueni'),
#     421: ('Wote', 'Kaiti', 'Makueni'),
#     422: ('Muvau/Kikuumini', 'Kaiti', 'Makueni'),
#     423: ('Mavindini', 'Kaiti', 'Makueni'),
#     424: ('Kitise/Kithuki', 'Kaiti', 'Makueni'),
#     425: ('Kathonzweni', 'Kaiti', 'Makueni'),
#     426: ('Nzau/Kilili/Kalamba', 'Kaiti', 'Makueni'),
#     427: ('Mbitini', 'Kaiti', 'Makueni'),
#     428: ('Kasikeu', 'Makueni', 'Makueni'),
#     429: ('Mukaa', 'Makueni', 'Makueni'),
#     430: ('Kiima Kiu/Kalanzoni', 'Makueni', 'Makueni'),
#     431: ('Masongaleni', 'Kibwezi East', 'Makueni'),
#     432: ('Mtito Andei', 'Kibwezi East', 'Makueni'),
#     433: ('Thange', 'Kibwezi East', 'Makueni'),
#     434: ('Ivingoni/Nzambani', 'Kibwezi East', 'Makueni'),
#     435: ('Makindu', 'Kibwezi West', 'Makueni'),
#     436: ('Nguumo', 'Kibwezi West', 'Makueni'),
#     437: ('Kikumbulyu North', 'Kibwezi West', 'Makueni'),
#     438: ('Kimumbulyu South', 'Kibwezi West', 'Makueni'),
#     439: ('Nguu/Masumba', 'Kibwezi West', 'Makueni'),
#     440: ('Emali/Mulala', 'Kibwezi West', 'Makueni'),
#     441: ('Engineer', 'Kinangop', 'Nyandarua'),
#     442: ('Gathara', 'Kinangop', 'Nyandarua'),
#     443: ('North Kinangop', 'Kinangop', 'Nyandarua'),
#     444: ('Murungaru', 'Kinangop', 'Nyandarua'),
#     445: ('Njabini/Kiburu', 'Kinangop', 'Nyandarua'),
#     446: ('Nyakio', 'Kinangop', 'Nyandarua'),
#     447: ('Githabai', 'Kinangop', 'Nyandarua'),
#     448: ('Magumu', 'Kinangop', 'Nyandarua'),
#     449: ('Wanjohi', 'Kipipiri', 'Nyandarua'),
#     450: ('Kipipiri', 'Kipipiri', 'Nyandarua'),
#     451: ('Geta', 'Kipipiri', 'Nyandarua'),
#     452: ('Githioro', 'Kipipiri', 'Nyandarua'),
#     453: ('Gathanji', 'Ol Kalou', 'Nyandarua'),
#     454: ('Gatima', 'Ol Kalou', 'Nyandarua'),
#     455: ('Weru', 'Ol Kalou', 'Nyandarua'),
#     456: ('Charagita', 'Ol Kalou', 'Nyandarua'),
#     457: ('Leshau/Pondo', 'Ol Jorok', 'Nyandarua'),
#     458: ('Kiriita', 'Ol Jorok', 'Nyandarua'),
#     459: ('Central', 'Ol Jorok', 'Nyandarua'),
#     460: ('Shamata', 'Ol Jorok', 'Nyandarua'),
#     461: ('Karau', 'Tetu', 'Nyeri'),
#     462: ('Kanjuiri Range', 'Tetu', 'Nyeri'),
#     463: ('Mirangine', 'Tetu', 'Nyeri'),
#     464: ('Kaimbaga', 'Tetu', 'Nyeri'),
#     465: ('Rurii', 'Tetu', 'Nyeri'),
#     466: ('Ruguru', 'Kieni', 'Nyeri'),
#     467: ('Magutu', 'Kieni', 'Nyeri'),
#     468: ('Iriani', 'Kieni', 'Nyeri'),
#     469: ('Konyu', 'Kieni', 'Nyeri'),
#     470: ('Kirimukuyu', 'Kieni', 'Nyeri'),
#     471: ('Karatina Town', 'Kieni', 'Nyeri'),
#     472: ('Mahiga', 'Mathira', 'Nyeri'),
#     473: ('Iria-Ini', 'Mathira', 'Nyeri'),
#     474: ('Chinga', 'Mathira', 'Nyeri'),
#     475: ('Karima', 'Mathira', 'Nyeri'),
#     476: ('Dedan Kimathi', 'Othaya', 'Nyeri'),
#     477: ('Wamagana', 'Othaya', 'Nyeri'),
#     478: ('Aguthi-Gaaki', 'Othaya', 'Nyeri'),
#     479: ('Gikondi', 'Mukurweini', 'Nyeri'),
#     480: ('Rugi', 'Mukurweini', 'Nyeri'),
#     481: ('Mukurwe-Ini West', 'Mukurweini', 'Nyeri'),
#     482: ('Mukurwe-Ini Central', 'Mukurweini', 'Nyeri'),
#     483: ('Kiganjo/Mathari', 'Nyeri Town', 'Nyeri'),
#     484: ('Rware', 'Nyeri Town', 'Nyeri'),
#     485: ('Gatitu/Muruguru', 'Nyeri Town', 'Nyeri'),
#     486: ("Ruring'u", 'Nyeri Town', 'Nyeri'),
#     487: ('Kamakwa/Mukaro', 'Nyeri Town', 'Nyeri'),
#     488: ('Mweiga', 'Mwea', 'Kirinyaga'),
#     489: ('Naromoro Kiamthaga', 'Mwea', 'Kirinyaga'),
#     490: ('Mwiyogo/Endara Sha', 'Mwea', 'Kirinyaga'),
#     491: ('Mugunda', 'Mwea', 'Kirinyaga'),
#     492: ('Gatarakwa', 'Mwea', 'Kirinyaga'),
#     493: ('Thegu River', 'Mwea', 'Kirinyaga'),
#     494: ('Kabaru', 'Mwea', 'Kirinyaga'),
#     495: ('Gakawa', 'Mwea', 'Kirinyaga'),
#     496: ('Mutira', 'Gichugu', 'Kirinyaga'),
#     497: ('Kanyekini', 'Gichugu', 'Kirinyaga'),
#     498: ('Kerugoya', 'Gichugu', 'Kirinyaga'),
#     499: ('Inoi', 'Gichugu', 'Kirinyaga'),
#     500: ('Mutithi', 'Ndia', 'Kirinyaga'),
#     501: ('Kangai', 'Ndia', 'Kirinyaga'),
#     502: ('Wamumu', 'Ndia', 'Kirinyaga'),
#     503: ('Nyangati', 'Ndia', 'Kirinyaga'),
#     504: ('Murindiko', 'Ndia', 'Kirinyaga'),
#     505: ('Gathigiriri', 'Ndia', 'Kirinyaga'),
#     506: ('Teberer', 'Ndia', 'Kirinyaga'),
#     507: ('Thiba', 'Ndia', 'Kirinyaga'),
#     508: ('Kabare Baragwi', 'Kirinyaga Central', 'Kirinyaga'),
#     509: ('Njukiini', 'Kirinyaga Central', 'Kirinyaga'),
#     510: ('Ngariama', 'Kirinyaga Central', 'Kirinyaga'),
#     511: ('Karumandi', 'Kirinyaga Central', 'Kirinyaga'),
#     512: ('Mukure', 'Kangema', "Murang'a"),
#     513: ('Kiine', 'Kangema', "Murang'a"),
#     514: ('Kariti', 'Kangema', "Murang'a"),
#     515: ('Ithanga', 'Mathioya', "Murang'a"),
#     516: ('Kakuzi/Mitubiri', 'Mathioya', "Murang'a"),
#     517: ('Mugumo-Ini', 'Mathioya', "Murang'a"),
#     518: ('Kihumbu-Ini', 'Mathioya', "Murang'a"),
#     519: ('Gatanga', 'Mathioya', "Murang'a"),
#     520: ('Kariara', 'Mathioya', "Murang'a"),
#     521: ("Ng'ararii", 'Kiharu', "Murang'a"),
#     522: ('Muruka', 'Kiharu', "Murang'a"),
#     523: ('Kangundu-Ini', 'Kiharu', "Murang'a"),
#     524: ('Gaichanjiru', 'Kiharu', "Murang'a"),
#     525: ('Ithiru', 'Kiharu', "Murang'a"),
#     526: ('Ruchu', 'Kiharu', "Murang'a"),
#     527: ('Kahumbu', 'Kigumo', "Murang'a"),
#     528: ('Muthithi', 'Kigumo', "Murang'a"),
#     529: ('Kigumo', 'Kigumo', "Murang'a"),
#     530: ('Kangari', 'Kigumo', "Murang'a"),
#     531: ('Kinyona', 'Kigumo', "Murang'a"),
#     532: ('Gituhi', 'Maragwa', "Murang'a"),
#     533: ('Kiru', 'Maragwa', "Murang'a"),
#     534: ('Kamacharia', 'Maragwa', "Murang'a"),
#     535: ('Wangu', 'Kandara', "Murang'a"),
#     536: ('Mugoiri', 'Kandara', "Murang'a"),
#     537: ('Mbiri', 'Kandara', "Murang'a"),
#     538: ('Township', 'Kandara', "Murang'a"),
#     539: ('Murarandia', 'Kandara', "Murang'a"),
#     540: ('Gaturi', 'Kandara', "Murang'a"),
#     541: ('Kanyenya-Ini', 'Gatundu South', 'Kiambu'),
#     542: ('Muguru', 'Gatundu South', 'Kiambu'),
#     543: ('Rwathia', 'Gatundu South', 'Kiambu'),
#     544: ('Kimorori/Wempa', 'Gatundu North', 'Kiambu'),
#     545: ('Makuyu', 'Gatundu North', 'Kiambu'),
#     546: ('Kambiti', 'Gatundu North', 'Kiambu'),
#     547: ('Kamahuha', 'Gatundu North', 'Kiambu'),
#     548: ('Ichagaki', 'Gatundu North', 'Kiambu'),
#     549: ('Nginda', 'Gatundu North', 'Kiambu'),
#     550: ('Gituamba', 'Juja', 'Kiambu'),
#     551: ('Githobokoni', 'Juja', 'Kiambu'),
#     552: ('Chania', 'Juja', 'Kiambu'),
#     553: ("Mang'u", 'Juja', 'Kiambu'),
#     554: ('Kiamwangi', 'Thika Town', 'Kiambu'),
#     555: ('Kiganjo', 'Thika Town', 'Kiambu'),
#     556: ('Ndarugu', 'Thika Town', 'Kiambu'),
#     557: ('Ngenda', 'Thika Town', 'Kiambu'),
#     558: ('Githunguri', 'Ruiru', 'Kiambu'),
#     559: ('Githiga', 'Ruiru', 'Kiambu'),
#     560: ('Ikinu', 'Ruiru', 'Kiambu'),
#     561: ('Ngewa', 'Ruiru', 'Kiambu'),
#     562: ('Komothai', 'Ruiru', 'Kiambu'),
#     563: ('Murera', 'Githunguri', 'Kiambu'),
#     564: ('Theta', 'Githunguri', 'Kiambu'),
#     565: ('Juja', 'Githunguri', 'Kiambu'),
#     566: ('Witeithie', 'Githunguri', 'Kiambu'),
#     567: ('Kalimoni', 'Githunguri', 'Kiambu'),
#     568: ('Gitaru', 'Kiambu', 'Kiambu'),
#     569: ('Muguga', 'Kiambu', 'Kiambu'),
#     570: ('Nyathuna', 'Kiambu', 'Kiambu'),
#     571: ('Kabete', 'Kiambu', 'Kiambu'),
#     572: ('Uthiru', 'Kiambu', 'Kiambu'),
#     573: ('Cianda', 'Kiambaa', 'Kiambu'),
#     574: ('Karuiri', 'Kiambaa', 'Kiambu'),
#     575: ('Ndenderu', 'Kiambaa', 'Kiambu'),
#     576: ('Muchatha', 'Kiambaa', 'Kiambu'),
#     577: ('Kihara', 'Kiambaa', 'Kiambu'),
#     578: ("Ting'ang'a", 'Kabete', 'Kiambu'),
#     579: ('Ndumberi', 'Kabete', 'Kiambu'),
#     580: ('Riabai', 'Kabete', 'Kiambu'),
#     581: ('Township', 'Kabete', 'Kiambu'),
#     582: ('Bibirioni', 'Kikuyu', 'Kiambu'),
#     583: ('Limuru Central', 'Kikuyu', 'Kiambu'),
#     584: ('Ndeiya', 'Kikuyu', 'Kiambu'),
#     585: ('Limuru East', 'Kikuyu', 'Kiambu'),
#     586: ('Ngecha Tigoni', 'Kikuyu', 'Kiambu'),
#     587: ('Karai', 'Limuru', 'Kiambu'),
#     588: ('Nachu', 'Limuru', 'Kiambu'),
#     589: ('Sigona', 'Limuru', 'Kiambu'),
#     590: ('Kikuyu', 'Limuru', 'Kiambu'),
#     591: ('Kinoo', 'Limuru', 'Kiambu'),
#     592: ('Kijabe', 'Lari', 'Kiambu'),
#     593: ('Nyanduma', 'Lari', 'Kiambu'),
#     594: ('Kamburu', 'Lari', 'Kiambu'),
#     595: ('Lari/Kirenga', 'Lari', 'Kiambu'),
#     596: ('Gitothua', 'Turkana North', 'Turkana'),
#     597: ('Biashara', 'Turkana North', 'Turkana'),
#     598: ('Gatongora', 'Turkana North', 'Turkana'),
#     599: ('Kahawa Sukari', 'Turkana North', 'Turkana'),
#     600: ('Kahawa Wendani', 'Turkana North', 'Turkana'),
#     601: ('Kiuu', 'Turkana North', 'Turkana'),
#     602: ('Mwiki', 'Turkana North', 'Turkana'),
#     603: ('Mwihoko', 'Turkana North', 'Turkana'),
#     604: ('Township', 'Turkana West', 'Turkana'),
#     605: ('Kamenu', 'Turkana West', 'Turkana'),
#     606: ('Hospital', 'Turkana West', 'Turkana'),
#     607: ('Gatuanyaga', 'Turkana West', 'Turkana'),
#     608: ('Ngoliba', 'Turkana West', 'Turkana'),
#     609: ('Kerio Delta', 'Turkana Central', 'Turkana'),
#     610: ("Kang'atotha", 'Turkana Central', 'Turkana'),
#     611: ('Kalokol', 'Turkana Central', 'Turkana'),
#     612: ('Lodwar Township', 'Turkana Central', 'Turkana'),
#     613: ('Kanamkemer', 'Turkana Central', 'Turkana'),
#     614: ('Kapedo/Napeito', 'Loima', 'Turkana'),
#     615: ('Katilia', 'Loima', 'Turkana'),
#     616: ('Lokori/Kochodin', 'Loima', 'Turkana'),
#     617: ('Kaeris', 'Turkana South', 'Turkana'),
#     618: ('Lake zone', 'Turkana South', 'Turkana'),
#     619: ('Lapur', 'Turkana South', 'Turkana'),
#     620: ('Kaaleng/kaikor', 'Turkana South', 'Turkana'),
#     621: ('Kibish', 'Turkana South', 'Turkana'),
#     622: ('Nakalale', 'Turkana South', 'Turkana'),
#     623: ('Kaputir', 'Turkana East', 'Turkana'),
#     624: ('Katilu', 'Turkana East', 'Turkana'),
#     625: ('Lobokat', 'Turkana East', 'Turkana'),
#     626: ('Kalapata', 'Turkana East', 'Turkana'),
#     627: ('Lokichar', 'Turkana East', 'Turkana'),
#     628: ('Kakuma', 'Kapenguria', 'West Pokot'),
#     629: ('Lopur', 'Kapenguria', 'West Pokot'),
#     630: ('Letea', 'Kapenguria', 'West Pokot'),
#     631: ('Songot', 'Kapenguria', 'West Pokot'),
#     632: ('Kalobeyei', 'Kapenguria', 'West Pokot'),
#     633: ('Lokichoggio', 'Kapenguria', 'West Pokot'),
#     634: ('Nanaam', 'Kapenguria', 'West Pokot'),
#     635: ('Kotaruk/Lobei', 'Sigor', 'West Pokot'),
#     636: ('Turkwel', 'Sigor', 'West Pokot'),
#     637: ('Loima', 'Sigor', 'West Pokot'),
#     638: ('Lokiriama/Loren Gippi', 'Sigor', 'West Pokot'),
#     639: ('Riwo', 'Kacheliba', 'West Pokot'),
#     640: ('Kapenguria', 'Kacheliba', 'West Pokot'),
#     641: ('Mnagei', 'Kacheliba', 'West Pokot'),
#     642: ('Siyoi', 'Kacheliba', 'West Pokot'),
#     643: ('Endugh', 'Kacheliba', 'West Pokot'),
#     644: ('Sook', 'Kacheliba', 'West Pokot'),
#     645: ('Sekerr', 'Pokot South', 'West Pokot'),
#     646: ('Masool', 'Pokot South', 'West Pokot'),
#     647: ('Lomut', 'Pokot South', 'West Pokot'),
#     648: ('Weiwei', 'Pokot South', 'West Pokot'),
#     649: ('Suam', 'Samburu West', 'Samburu'),
#     650: ('Kodich', 'Samburu West', 'Samburu'),
#     651: ('Kasei', 'Samburu West', 'Samburu'),
#     652: ('Kapchok', 'Samburu West', 'Samburu'),
#     653: ('Kiwawa', 'Samburu West', 'Samburu'),
#     654: ('Alale', 'Samburu West', 'Samburu'),
#     655: ('Chepareria', 'Samburu North', 'Samburu'),
#     656: ('Batei', 'Samburu North', 'Samburu'),
#     657: ('Lelan', 'Samburu North', 'Samburu'),
#     658: ('Tapach', 'Samburu North', 'Samburu'),
#     659: ('Waso', 'Samburu East', 'Samburu'),
#     660: ('Wamba West', 'Samburu East', 'Samburu'),
#     661: ('Wamba East', 'Samburu East', 'Samburu'),
#     662: ('Wamba North', 'Samburu East', 'Samburu'),
#     663: ('El-Barta', 'Kwanza', 'Trans Nzoia'),
#     664: ('Nachola', 'Kwanza', 'Trans Nzoia'),
#     665: ('Ndoto', 'Kwanza', 'Trans Nzoia'),
#     666: ('Nyiro', 'Kwanza', 'Trans Nzoia'),
#     667: ('Angata Nanyokie', 'Kwanza', 'Trans Nzoia'),
#     668: ('Baawa', 'Kwanza', 'Trans Nzoia'),
#     669: ('Lodokejek', 'Endebess', 'Trans Nzoia'),
#     670: ('Suguta Marmar', 'Endebess', 'Trans Nzoia'),
#     671: ('Maralal', 'Endebess', 'Trans Nzoia'),
#     672: ('Loosuk', 'Endebess', 'Trans Nzoia'),
#     673: ('Poro', 'Endebess', 'Trans Nzoia'),
#     674: ('Sinyerere', 'Saboti', 'Trans Nzoia'),
#     675: ('Makutano', 'Saboti', 'Trans Nzoia'),
#     676: ('Kaplamai', 'Saboti', 'Trans Nzoia'),
#     677: ('Motosiet', 'Saboti', 'Trans Nzoia'),
#     678: ('Cherangany/Suwerwa', 'Saboti', 'Trans Nzoia'),
#     679: ('Chepsiro/Kiptoror', 'Saboti', 'Trans Nzoia'),
#     680: ('Sitatunga', 'Saboti', 'Trans Nzoia'),
#     681: ('Kapomboi', 'Kiminini', 'Trans Nzoia'),
#     682: ('Kwanza', 'Kiminini', 'Trans Nzoia'),
#     683: ('Keiyo', 'Kiminini', 'Trans Nzoia'),
#     684: ('Bidii', 'Kiminini', 'Trans Nzoia'),
#     685: ('Chepchoina', 'Cherangany', 'Trans Nzoia'),
#     686: ('Endebess', 'Cherangany', 'Trans Nzoia'),
#     687: ('Matumbei', 'Cherangany', 'Trans Nzoia'),
#     688: ('Kinyoro', 'Soy', 'Uasin Gishu'),
#     689: ('Matisi', 'Soy', 'Uasin Gishu'),
#     690: ('Tuwani', 'Soy', 'Uasin Gishu'),
#     691: ('Saboti', 'Soy', 'Uasin Gishu'),
#     692: ('Machewa', 'Soy', 'Uasin Gishu'),
#     693: ('Kiminini', 'Turbo', 'Uasin Gishu'),
#     694: ('Waitaluk', 'Turbo', 'Uasin Gishu'),
#     695: ('Sirende', 'Turbo', 'Uasin Gishu'),
#     696: ('Hospital', 'Turbo', 'Uasin Gishu'),
#     697: ('Sikhendu', 'Turbo', 'Uasin Gishu'),
#     698: ('Nabiswa', 'Turbo', 'Uasin Gishu'),
#     699: ('Kapsoya', 'Moiben', 'Uasin Gishu'),
#     700: ('Kaptagat', 'Moiben', 'Uasin Gishu'),
#     701: ('Ainabkoi/Olare', 'Moiben', 'Uasin Gishu'),
#     702: ('Simat/Kapseret', 'Ainabkoi', 'Uasin Gishu'),
#     703: ('Kipkenyo', 'Ainabkoi', 'Uasin Gishu'),
#     704: ('Ngeria', 'Ainabkoi', 'Uasin Gishu'),
#     705: ('Megun', 'Ainabkoi', 'Uasin Gishu'),
#     706: ('Langas', 'Ainabkoi', 'Uasin Gishu'),
#     707: ('Racecourse', 'Kapseret', 'Uasin Gishu'),
#     708: ('Cheptiret/Kipchamo', 'Kapseret', 'Uasin Gishu'),
#     709: ('Tulwet/Chuiyat', 'Kapseret', 'Uasin Gishu'),
#     710: ('Tarakwa', 'Kapseret', 'Uasin Gishu'),
#     711: ('Tembelio', 'Kesses', 'Uasin Gishu'),
#     712: ('Sergoit', 'Kesses', 'Uasin Gishu'),
#     713: ('Karuna/Meibeki', 'Kesses', 'Uasin Gishu'),
#     714: ('Moiben', 'Kesses', 'Uasin Gishu'),
#     715: ('Kimumu', 'Kesses', 'Uasin Gishu'),
#     716: ("Moi's Bridge", 'Marakwet East', 'Elgeyo-Marakwet'),
#     717: ('Kapkures', 'Marakwet East', 'Elgeyo-Marakwet'),
#     718: ('Ziwa', 'Marakwet East', 'Elgeyo-Marakwet'),
#     719: ('Segero/Barsombe', 'Marakwet East', 'Elgeyo-Marakwet'),
#     720: ('Kipsom Ba', 'Marakwet East', 'Elgeyo-Marakwet'),
#     721: ('Soy', 'Marakwet East', 'Elgeyo-Marakwet'),
#     722: ('Kuinet/Kapsuswa', 'Marakwet East', 'Elgeyo-Marakwet'),
#     723: ('Ngenyilel', 'Marakwet West', 'Elgeyo-Marakwet'),
#     724: ('Tapsagoi', 'Marakwet West', 'Elgeyo-Marakwet'),
#     725: ('Kamagut', 'Marakwet West', 'Elgeyo-Marakwet'),
#     726: ('Kiplombe', 'Marakwet West', 'Elgeyo-Marakwet'),
#     727: ('Kapsaos', 'Marakwet West', 'Elgeyo-Marakwet'),
#     728: ('Huruma', 'Marakwet West', 'Elgeyo-Marakwet'),
#     729: ('Emsoo', 'Keiyo North', 'Elgeyo-Marakwet'),
#     730: ('Kamariny', 'Keiyo North', 'Elgeyo-Marakwet'),
#     731: ('Kapchemutwa', 'Keiyo North', 'Elgeyo-Marakwet'),
#     732: ('Tambach', 'Keiyo North', 'Elgeyo-Marakwet'),
#     733: ('Kaptarakwa', 'Keiyo South', 'Elgeyo-Marakwet'),
#     734: ('Chepkorio', 'Keiyo South', 'Elgeyo-Marakwet'),
#     735: ('Soy North', 'Keiyo South', 'Elgeyo-Marakwet'),
#     736: ('Soy South', 'Keiyo South', 'Elgeyo-Marakwet'),
#     737: ('Kabiemit', 'Keiyo South', 'Elgeyo-Marakwet'),
#     738: ('Metkei', 'Keiyo South', 'Elgeyo-Marakwet'),
#     739: ('Kapyego', 'Tinderet', 'Nandi'),
#     740: ('Sambirir', 'Tinderet', 'Nandi'),
#     741: ('Endo', 'Tinderet', 'Nandi'),
#     742: ('Embobut / Embulot', 'Tinderet', 'Nandi'),
#     743: ('Kapsowar', 'Aldai', 'Nandi'),
#     744: ('Lelan', 'Aldai', 'Nandi'),
#     745: ('Sengwer', 'Aldai', 'Nandi'),
#     746: ("Cherang'any/Chebororwa", 'Aldai', 'Nandi'),
#     747: ('Moiben/Kuserwo', 'Aldai', 'Nandi'),
#     748: ('Arror', 'Aldai', 'Nandi'),
#     749: ('Kabwareng', 'Nandi Hills', 'Nandi'),
#     750: ('Terik', 'Nandi Hills', 'Nandi'),
#     751: ('Kemeloi-Maraba', 'Nandi Hills', 'Nandi'),
#     752: ('Kobujoi', 'Nandi Hills', 'Nandi'),
#     753: ('Kaptumo-Kaboi', 'Nandi Hills', 'Nandi'),
#     754: ('Koyo-Ndurio', 'Nandi Hills', 'Nandi'),
#     755: ("Chemundu/Kapng'etuny", 'Chesumei', 'Nandi'),
#     756: ('Kosirai', 'Chesumei', 'Nandi'),
#     757: ('Lelmokwo/Ngechek', 'Chesumei', 'Nandi'),
#     758: ('Kaptel/Kamoiywo', 'Chesumei', 'Nandi'),
#     759: ('Kiptuya', 'Chesumei', 'Nandi'),
#     760: ('Chepkumia', 'Emgwen', 'Nandi'),
#     761: ('Kapkangani', 'Emgwen', 'Nandi'),
#     762: ('Kapsabet', 'Emgwen', 'Nandi'),
#     763: ('Kilibwoni', 'Emgwen', 'Nandi'),
#     764: ('Chepterwai', 'Mosop', 'Nandi'),
#     765: ('Kipkaren', 'Mosop', 'Nandi'),
#     766: ('Kurgung/ Surungai', 'Mosop', 'Nandi'),
#     767: ('Kabiyet', 'Mosop', 'Nandi'),
#     768: ('Ndalat', 'Mosop', 'Nandi'),
#     769: ('Kabisaga', 'Mosop', 'Nandi'),
#     770: ('Sangalo/Kebulonik', 'Mosop', 'Nandi'),
#     771: ('Nandi Hills', 'Tiaty', 'Baringo'),
#     772: ('Chepkunyuk', 'Tiaty', 'Baringo'),
#     773: ("Ol'lessos", 'Tiaty', 'Baringo'),
#     774: ('Kapchorua', 'Tiaty', 'Baringo'),
#     775: ('Songhor/Soba', 'Baringo North', 'Baringo'),
#     776: ('Tindiret', 'Baringo North', 'Baringo'),
#     777: ('Chemelil/Chemase', 'Baringo North', 'Baringo'),
#     778: ('Kapsimotwo', 'Baringo North', 'Baringo'),
#     779: ('Kabarnet', 'Baringo Central', 'Baringo'),
#     780: ('Sacho', 'Baringo Central', 'Baringo'),
#     781: ('Tenges', 'Baringo Central', 'Baringo'),
#     782: ('Ewalel/Chapcha', 'Baringo Central', 'Baringo'),
#     783: ('Kapropita', 'Baringo Central', 'Baringo'),
#     784: ('Barwessa', 'Baringo South', 'Baringo'),
#     785: ('Kabartonjo', 'Baringo South', 'Baringo'),
#     786: ('Saimo/Kipsaraman', 'Baringo South', 'Baringo'),
#     787: ('Saimo/Soi', 'Baringo South', 'Baringo'),
#     788: ('Bartabwa', 'Baringo South', 'Baringo'),
#     789: ('Marigat', 'Mogotio', 'Baringo'),
#     790: ('Ilchamus', 'Mogotio', 'Baringo'),
#     791: ('Mochongoi', 'Mogotio', 'Baringo'),
#     792: ('Mukutani', 'Mogotio', 'Baringo'),
#     793: ('Lembus', 'Eldama Ravine', 'Baringo'),
#     794: ('Lembus Kwen', 'Eldama Ravine', 'Baringo'),
#     795: ('Ravine', 'Eldama Ravine', 'Baringo'),
#     796: ('Mumberes/Maji Mazuri', 'Eldama Ravine', 'Baringo'),
#     797: ('Lembus /Pekerra', 'Eldama Ravine', 'Baringo'),
#     798: ('Mogotio', 'Laikipia West', 'Laikipia'),
#     799: ('Emining', 'Laikipia West', 'Laikipia'),
#     800: ('Kisanana', 'Laikipia West', 'Laikipia'),
#     801: ('Tirioko', 'Laikipia East', 'Laikipia'),
#     802: ('Kolowa', 'Laikipia East', 'Laikipia'),
#     803: ('Ribkwo', 'Laikipia East', 'Laikipia'),
#     804: ('Silale', 'Laikipia East', 'Laikipia'),
#     805: ('Loiyamorock', 'Laikipia East', 'Laikipia'),
#     806: ('Tangulbei/Korossi', 'Laikipia East', 'Laikipia'),
#     807: ('Churo/Amaya', 'Laikipia East', 'Laikipia'),
#     808: ('Sosian', 'Laikipia North', 'Laikipia'),
#     809: ('Segera', 'Laikipia North', 'Laikipia'),
#     810: ('Mugogodo West', 'Laikipia North', 'Laikipia'),
#     811: ('Mugogodo East', 'Laikipia North', 'Laikipia'),
#     812: ('Ngobit', 'Molo', 'Nakuru'),
#     813: ('Tigithi', 'Molo', 'Nakuru'),
#     814: ('Thingithu', 'Molo', 'Nakuru'),
#     815: ('Nanyuki', 'Molo', 'Nakuru'),
#     816: ('Umande', 'Molo', 'Nakuru'),
#     817: ('Ol-Moran', 'Njoro', 'Nakuru'),
#     818: ('Rumuruti', 'Njoro', 'Nakuru'),
#     819: ('Township', 'Njoro', 'Nakuru'),
#     820: ('Githiga', 'Njoro', 'Nakuru'),
#     821: ('Marmanet', 'Njoro', 'Nakuru'),
#     822: ('Igwamiti Salama', 'Njoro', 'Nakuru'),
#     823: ('Biashara', 'Naivasha', 'Nakuru'),
#     824: ('Kivumbini', 'Naivasha', 'Nakuru'),
#     825: ('Flamingo', 'Naivasha', 'Nakuru'),
#     826: ('Menengai', 'Naivasha', 'Nakuru'),
#     827: ('Nakuru East', 'Naivasha', 'Nakuru'),
#     828: ('Barut', 'Gilgil', 'Nakuru'),
#     829: ('London', 'Gilgil', 'Nakuru'),
#     830: ('Kaptembwo', 'Gilgil', 'Nakuru'),
#     831: ('Kapkures', 'Gilgil', 'Nakuru'),
#     832: ('Rhoda', 'Gilgil', 'Nakuru'),
#     833: ('Shaabab', 'Gilgil', 'Nakuru'),
#     834: ('Mau Narok', 'Kuresoi South', 'Nakuru'),
#     835: ('Mauche', 'Kuresoi South', 'Nakuru'),
#     836: ('Kihingo', 'Kuresoi South', 'Nakuru'),
#     837: ('Nessuit', 'Kuresoi South', 'Nakuru'),
#     838: ('Lare', 'Kuresoi South', 'Nakuru'),
#     839: ('Njoro', 'Kuresoi South', 'Nakuru'),
#     840: ('Mariashoni', 'Kuresoi North', 'Nakuru'),
#     841: ('Elburgon', 'Kuresoi North', 'Nakuru'),
#     842: ('Turi', 'Kuresoi North', 'Nakuru'),
#     843: ('Molo', 'Kuresoi North', 'Nakuru'),
#     844: ('Gilgil', 'Subukia', 'Nakuru'),
#     845: ('Elementaita', 'Subukia', 'Nakuru'),
#     846: ('Mbaruk/Eburu', 'Subukia', 'Nakuru'),
#     847: ('Malewa West', 'Subukia', 'Nakuru'),
#     848: ('Murindati', 'Subukia', 'Nakuru'),
#     849: ('Biashara', 'Rongai', 'Nakuru'),
#     850: ('Hells Gate', 'Rongai', 'Nakuru'),
#     851: ('Lake View', 'Rongai', 'Nakuru'),
#     852: ('Maiella', 'Rongai', 'Nakuru'),
#     853: ('Mai Mahiu', 'Rongai', 'Nakuru'),
#     854: ('Olkaria', 'Rongai', 'Nakuru'),
#     855: ('Naivasha East', 'Rongai', 'Nakuru'),
#     856: ('Viwandani', 'Rongai', 'Nakuru'),
#     857: ('Kiptororo', 'Bahati', 'Nakuru'),
#     858: ('Nyota', 'Bahati', 'Nakuru'),
#     859: ('Sirikwa', 'Bahati', 'Nakuru'),
#     860: ('Kamara', 'Bahati', 'Nakuru'),
#     861: ('Amalo', 'Nakuru Town West', 'Nakuru'),
#     862: ('Keringet', 'Nakuru Town West', 'Nakuru'),
#     863: ('Kiptagich', 'Nakuru Town West', 'Nakuru'),
#     864: ('Tinet', 'Nakuru Town West', 'Nakuru'),
#     865: ('Dundori', 'Nakuru Town East', 'Nakuru'),
#     866: ('Kabatini', 'Nakuru Town East', 'Nakuru'),
#     867: ('Kiamaina', 'Nakuru Town East', 'Nakuru'),
#     868: ('Lanet/Umoja', 'Nakuru Town East', 'Nakuru'),
#     869: ('Bahati', 'Nakuru Town East', 'Nakuru'),
#     870: ('Menengai West', 'Kilgoris', 'Narok'),
#     871: ('Soin', 'Kilgoris', 'Narok'),
#     872: ('Visoi', 'Kilgoris', 'Narok'),
#     873: ('Mosop', 'Kilgoris', 'Narok'),
#     874: ('Solai', 'Kilgoris', 'Narok'),
#     875: ('Subukia', 'Emurua Dikirr', 'Narok'),
#     876: ('Waseges', 'Emurua Dikirr', 'Narok'),
#     877: ('Kabazi', 'Emurua Dikirr', 'Narok'),
#     878: ('Olpusimoru', 'Narok North', 'Narok'),
#     879: ('Olokurto', 'Narok North', 'Narok'),
#     880: ('Narok Town', 'Narok North', 'Narok'),
#     881: ("Nkareta'Olorropil", 'Narok North', 'Narok'),
#     882: ('Melili', 'Narok North', 'Narok'),
#     883: ('Majimoto/Naroos', 'Narok East', 'Narok'),
#     884: ("Uraololulung'a", 'Narok East', 'Narok'),
#     885: ('Melelo', 'Narok East', 'Narok'),
#     886: ('Loita', 'Narok East', 'Narok'),
#     887: ('Sogoo', 'Narok East', 'Narok'),
#     888: ('Sagamian', 'Narok East', 'Narok'),
#     889: ('Mosiro', 'Narok South', 'Narok'),
#     890: ('Ildamat', 'Narok South', 'Narok'),
#     891: ('Keekonyokie', 'Narok South', 'Narok'),
#     892: ('Suswa', 'Narok South', 'Narok'),
#     893: ('Ilmotiok', 'Narok West', 'Narok'),
#     894: ('Mara', 'Narok West', 'Narok'),
#     895: ('Siana', 'Narok West', 'Narok'),
#     896: ('Naikarra', 'Narok West', 'Narok'),
#     897: ('Kilgoris Central', 'Kajiado North', 'Kajiado'),
#     898: ('Keyian', 'Kajiado North', 'Kajiado'),
#     899: ('Angata Barikoi', 'Kajiado North', 'Kajiado'),
#     900: ('Shankoe', 'Kajiado North', 'Kajiado'),
#     901: ('Kimintet', 'Kajiado North', 'Kajiado'),
#     902: ('Lolgorian', 'Kajiado North', 'Kajiado'),
#     903: ('Ilkerin', 'Kajiado Central', 'Kajiado'),
#     904: ('Ololmasani', 'Kajiado Central', 'Kajiado'),
#     905: ('Mogondo', 'Kajiado Central', 'Kajiado'),
#     906: ('Kapsasian', 'Kajiado Central', 'Kajiado'),
#     907: ('Purko', 'Kajiado East', 'Kajiado'),
#     908: ('Ildamat', 'Kajiado East', 'Kajiado'),
#     909: ('Dalalekutuk', 'Kajiado East', 'Kajiado'),
#     910: ('Matapato North', 'Kajiado East', 'Kajiado'),
#     911: ('Matapato South', 'Kajiado East', 'Kajiado'),
#     912: ('Kaputiei North', 'Kajiado West', 'Kajiado'),
#     913: ('Kitengela', 'Kajiado West', 'Kajiado'),
#     914: ('Oloosirkon/Sholinke', 'Kajiado West', 'Kajiado'),
#     915: ('Kenyawa-Poka', 'Kajiado West', 'Kajiado'),
#     916: ('Imaroro', 'Kajiado West', 'Kajiado'),
#     917: ('Olkeri', 'Kajiado South', 'Kajiado'),
#     918: ('Ongata Rongai', 'Kajiado South', 'Kajiado'),
#     919: ('Nkaimurunya', 'Kajiado South', 'Kajiado'),
#     920: ('Oloolua', 'Kajiado South', 'Kajiado'),
#     921: ('Ngong', 'Kajiado South', 'Kajiado'),
#     922: ('Keekonyokie', 'Ainamoi', 'Kericho'),
#     923: ('Iloodokilani', 'Ainamoi', 'Kericho'),
#     924: ('Magadi', 'Ainamoi', 'Kericho'),
#     925: ("Ewuaso Oonkidong'i", 'Ainamoi', 'Kericho'),
#     926: ('Mosiro', 'Ainamoi', 'Kericho'),
#     927: ('Entonet/Lenkisi', 'Belgut', 'Kericho'),
#     928: ('Mbirikani/Eselen', 'Belgut', 'Kericho'),
#     929: ('Keikuku', 'Belgut', 'Kericho'),
#     930: ('Rombo', 'Belgut', 'Kericho'),
#     931: ('Kimana', 'Belgut', 'Kericho'),
#     932: ('Kapsoit', 'Sigowet/Soin', 'Kericho'),
#     933: ('Ainamoi', 'Sigowet/Soin', 'Kericho'),
#     934: ('Kipchebor', 'Sigowet/Soin', 'Kericho'),
#     935: ('Kapkugerwet', 'Sigowet/Soin', 'Kericho'),
#     936: ('Kipchimchim', 'Sigowet/Soin', 'Kericho'),
#     937: ('Kapsaos', 'Sigowet/Soin', 'Kericho'),
#     938: ('Waldai', 'Kipkelion East', 'Kericho'),
#     939: ('Kabianga', 'Kipkelion East', 'Kericho'),
#     940: ('Cheptororiet/Seretut', 'Kipkelion East', 'Kericho'),
#     941: ('Chaik', 'Kipkelion East', 'Kericho'),
#     942: ('Kapsuser', 'Kipkelion East', 'Kericho'),
#     943: ('Kisiara', 'Kipkelion West', 'Kericho'),
#     944: ('Tebesonik', 'Kipkelion West', 'Kericho'),
#     945: ('Cheboin', 'Kipkelion West', 'Kericho'),
#     946: ('Chemosot', 'Kipkelion West', 'Kericho'),
#     947: ('Litein', 'Kipkelion West', 'Kericho'),
#     948: ('Cheplanget', 'Kipkelion West', 'Kericho'),
#     949: ('Kapkatet', 'Kipkelion West', 'Kericho'),
#     950: ('Londiani', 'Sotik', 'Bomet'),
#     951: ('Kedowa/Kimugul', 'Sotik', 'Bomet'),
#     952: ('Chepseon', 'Sotik', 'Bomet'),
#     953: ('Tendeno/Sorget', 'Sotik', 'Bomet'),
#     954: ('Kunyak', 'Chepalungu', 'Bomet'),
#     955: ('Kamasian', 'Chepalungu', 'Bomet'),
#     956: ('Kipkelion', 'Chepalungu', 'Bomet'),
#     957: ('Chilchila', 'Chepalungu', 'Bomet'),
#     958: ('Sigowet', 'Bomet East', 'Bomet'),
#     959: ('Kaplelartet', 'Bomet East', 'Bomet'),
#     960: ('Soliat', 'Bomet East', 'Bomet'),
#     961: ('Soin', 'Bomet East', 'Bomet'),
#     962: ('Ndanai/Abosi', 'Bomet Central', 'Bomet'),
#     963: ('Chemagel', 'Bomet Central', 'Bomet'),
#     964: ('Kipsonoi', 'Bomet Central', 'Bomet'),
#     965: ('Apletundo', 'Bomet Central', 'Bomet'),
#     966: ('Rongena/Manare T', 'Bomet Central', 'Bomet'),
#     967: ('Silibwet Township', 'Konoin', 'Bomet'),
#     968: ('Ndaraweta', 'Konoin', 'Bomet'),
#     969: ('Singorwet', 'Konoin', 'Bomet'),
#     970: ('Chesoen', 'Konoin', 'Bomet'),
#     971: ('Mutarakwa', 'Konoin', 'Bomet'),
#     972: ('Merigi', 'Lugari', 'Kakamega'),
#     973: ('Kembu', 'Lugari', 'Kakamega'),
#     974: ('Longisa', 'Lugari', 'Kakamega'),
#     975: ('Kipreres', 'Lugari', 'Kakamega'),
#     976: ('Chemaner', 'Lugari', 'Kakamega'),
#     977: ("Kong'asis", 'Likuyani', 'Kakamega'),
#     978: ('Nyangores', 'Likuyani', 'Kakamega'),
#     979: ('Sigor', 'Likuyani', 'Kakamega'),
#     980: ('Chebunyo', 'Likuyani', 'Kakamega'),
#     981: ('Siongiroi', 'Likuyani', 'Kakamega'),
#     982: ('Chepchabas', 'Malava', 'Kakamega'),
#     983: ('Kimulot', 'Malava', 'Kakamega'),
#     984: ('Mogogosiek', 'Malava', 'Kakamega'),
#     985: ('Boito', 'Malava', 'Kakamega'),
#     986: ('Embomos', 'Malava', 'Kakamega'),
#     987: ('Marama West', 'Lurambi', 'Kakamega'),
#     988: ('Marama Central', 'Lurambi', 'Kakamega'),
#     989: ('Marenyo-Shianda', 'Lurambi', 'Kakamega'),
#     990: ('Maram North', 'Lurambi', 'Kakamega'),
#     991: ('Marama South', 'Lurambi', 'Kakamega'),
#     992: ('Idakho South', 'Navakholo', 'Kakamega'),
#     993: ('Idakho East', 'Navakholo', 'Kakamega'),
#     994: ('Idakho North', 'Navakholo', 'Kakamega'),
#     995: ('Idakho Central', 'Navakholo', 'Kakamega'),
#     996: ('Kisa North', 'Mumias West', 'Kakamega'),
#     997: ('Kisa East', 'Mumias West', 'Kakamega'),
#     998: ('Kisa West', 'Mumias West', 'Kakamega'),
#     999: ('Kisa Central', 'Mumias West', 'Kakamega'),
#     1000: ('Butsotso East', 'Mumias East', 'Kakamega'),
#     1001: ('Butsotso South', 'Mumias East', 'Kakamega'),
#     1002: ('Butsotso Central', 'Mumias East', 'Kakamega'),
#     1003: ('Sheywe', 'Mumias East', 'Kakamega'),
#     1004: ('Mahiakalo', 'Mumias East', 'Kakamega'),
#     1005: ('Shirere', 'Mumias East', 'Kakamega'),
#     1006: ('Likuyani', 'Matungu', 'Kakamega'),
#     1007: ('Sango', 'Matungu', 'Kakamega'),
#     1008: ('Kongoni', 'Matungu', 'Kakamega'),
#     1009: ('Nzoia', 'Matungu', 'Kakamega'),
#     1010: ('Sinoko', 'Matungu', 'Kakamega'),
#     1011: ('West Kabras', 'Butere', 'Kakamega'),
#     1012: ('Chemuche East', 'Butere', 'Kakamega'),
#     1013: ('Kabras', 'Butere', 'Kakamega'),
#     1014: ('Butali/Chegulo', 'Butere', 'Kakamega'),
#     1015: ('Manda-Shivanga', 'Butere', 'Kakamega'),
#     1016: ('Shirugu-Mugai', 'Butere', 'Kakamega'),
#     1017: ('South Kabras', 'Butere', 'Kakamega'),
#     1018: ('Koyonzo', 'Khwisero', 'Kakamega'),
#     1019: ('Kholera', 'Khwisero', 'Kakamega'),
#     1020: ('Khalaba', 'Khwisero', 'Kakamega'),
#     1021: ('Mayoni', 'Khwisero', 'Kakamega'),
#     1022: ('Namamali', 'Khwisero', 'Kakamega'),
#     1023: ('Lusheya/Lubinu', 'Shinyalu', 'Kakamega'),
#     1024: ('Malaha/Isongo/Makunga', 'Shinyalu', 'Kakamega'),
#     1025: ('East Wanga', 'Shinyalu', 'Kakamega'),
#     1026: ('Mumias Central', 'Ikolomani', 'Kakamega'),
#     1027: ('Mumias North', 'Ikolomani', 'Kakamega'),
#     1028: ('Etenje', 'Ikolomani', 'Kakamega'),
#     1029: ('Musanda', 'Ikolomani', 'Kakamega'),
#     1030: ('Ingostse-Mathia', 'Vihiga', 'Vihiga'),
#     1031: ('Shinoyi-Shikomari', 'Vihiga', 'Vihiga'),
#     1032: ('Esumeyia', 'Vihiga', 'Vihiga'),
#     1033: ('Bunyala West', 'Vihiga', 'Vihiga'),
#     1034: ('Bunyal East', 'Vihiga', 'Vihiga'),
#     1035: ('Bunyala Central', 'Vihiga', 'Vihiga'),
#     1036: ('Mautuma', 'Sabatia', 'Vihiga'),
#     1037: ('Lugari', 'Sabatia', 'Vihiga'),
#     1038: ('Lumakanda', 'Sabatia', 'Vihiga'),
#     1039: ('Chekalini', 'Sabatia', 'Vihiga'),
#     1040: ('Chevaywa', 'Sabatia', 'Vihiga'),
#     1041: ('Lawandeti', 'Sabatia', 'Vihiga'),
#     1042: ('Mautuma', 'Hamisi', 'Vihiga'),
#     1043: ('Lugari', 'Hamisi', 'Vihiga'),
#     1044: ('Lumakanda', 'Hamisi', 'Vihiga'),
#     1045: ('Chekalini', 'Hamisi', 'Vihiga'),
#     1046: ('Chevaywa', 'Hamisi', 'Vihiga'),
#     1047: ('Lawandeti', 'Hamisi', 'Vihiga'),
#     1048: ('North East Bunyore', 'Luanda', 'Vihiga'),
#     1049: ('Central Bunyore', 'Luanda', 'Vihiga'),
#     1050: ('West Bunyore', 'Luanda', 'Vihiga'),
#     1051: ('Shiru', 'Emuhaya', 'Vihiga'),
#     1052: ('Gisambai', 'Emuhaya', 'Vihiga'),
#     1053: ('Shamakhokho', 'Emuhaya', 'Vihiga'),
#     1054: ('Banja', 'Emuhaya', 'Vihiga'),
#     1055: ('Muhudi', 'Emuhaya', 'Vihiga'),
#     1056: ('Tambaa', 'Emuhaya', 'Vihiga'),
#     1057: ('Jepkoyai', 'Emuhaya', 'Vihiga'),
#     1058: ('Lyaduywa/Izava', 'Mt. Elgon', 'Bungoma'),
#     1059: ('West Sabatia', 'Mt. Elgon', 'Bungoma'),
#     1060: ('Chavakali', 'Mt. Elgon', 'Bungoma'),
#     1061: ('North Maragoli', 'Mt. Elgon', 'Bungoma'),
#     1062: ('Wodanga', 'Mt. Elgon', 'Bungoma'),
#     1063: ('Busali', 'Mt. Elgon', 'Bungoma'),
#     1064: ('Lugaga-Wamuluma', 'Sirisia', 'Bungoma'),
#     1065: ('South Maragoli', 'Sirisia', 'Bungoma'),
#     1066: ('Central Maragoli', 'Sirisia', 'Bungoma'),
#     1067: ('Mungoma', 'Sirisia', 'Bungoma'),
#     1068: ('Luanda Township', 'Kabuchai', 'Bungoma'),
#     1069: ('Wemilabi', 'Kabuchai', 'Bungoma'),
#     1070: ('Mwibona', 'Kabuchai', 'Bungoma'),
#     1071: ('Luanda South', 'Kabuchai', 'Bungoma'),
#     1072: ('Emabungo', 'Kabuchai', 'Bungoma'),
#     1073: ('Bumula', 'Bumula', 'Bungoma'),
#     1074: ('Khasoko', 'Bumula', 'Bungoma'),
#     1075: ('Kabula', 'Bumula', 'Bungoma'),
#     1076: ('Kimaeti', 'Bumula', 'Bungoma'),
#     1077: ('South Bukusu', 'Bumula', 'Bungoma'),
#     1078: ('Siboti', 'Bumula', 'Bungoma'),
#     1079: ('Bukembe West', 'Kanduyi', 'Bungoma'),
#     1080: ('Bukembe East', 'Kanduyi', 'Bungoma'),
#     1081: ('Township', 'Kanduyi', 'Bungoma'),
#     1082: ('Khalaba', 'Kanduyi', 'Bungoma'),
#     1083: ('Musikoma', 'Kanduyi', 'Bungoma'),
#     1084: ("East Snag'alo", 'Kanduyi', 'Bungoma'),
#     1085: ('Marakatu', 'Kanduyi', 'Bungoma'),
#     1086: ('Tuuti', 'Kanduyi', 'Bungoma'),
#     1087: ("West Sang'alo", 'Kanduyi', 'Bungoma'),
#     1088: ('Mihuu', 'Webuye East', 'Bungoma'),
#     1089: ('Ndivisi', 'Webuye East', 'Bungoma'),
#     1090: ('Maraka', 'Webuye East', 'Bungoma'),
#     1091: ('Sitikho', 'Webuye West', 'Bungoma'),
#     1092: ('Matulo', 'Webuye West', 'Bungoma'),
#     1093: ('Bokoli', 'Webuye West', 'Bungoma'),
#     1094: ('Cheptais', 'Kimilili', 'Bungoma'),
#     1095: ('Chesikaki', 'Kimilili', 'Bungoma'),
#     1096: ('Chepyuk', 'Kimilili', 'Bungoma'),
#     1097: ('Kapkateny', 'Kimilili', 'Bungoma'),
#     1098: ('Kaptama', 'Kimilili', 'Bungoma'),
#     1099: ('Elgon', 'Kimilili', 'Bungoma'),
#     1100: ('Namwela', 'Tongaren', 'Bungoma'),
#     1101: ('Malakisi/South Kulisiru', 'Tongaren', 'Bungoma'),
#     1102: ('Lwandanyi', 'Tongaren', 'Bungoma'),
#     1103: ('Mbakalo', 'Teso North', 'Busia'),
#     1104: ('Naitiri/Kabuyefwe', 'Teso North', 'Busia'),
#     1105: ('Milima', 'Teso North', 'Busia'),
#     1106: ('Ndalu/Tabani', 'Teso North', 'Busia'),
#     1107: ('Tongaren', 'Teso North', 'Busia'),
#     1108: ('Soysambu/Mitua', 'Teso North', 'Busia'),
#     1109: ('Kabuchai/Chwele', 'Teso South', 'Busia'),
#     1110: ('West Nalondo', 'Teso South', 'Busia'),
#     1111: ('Bwake/Luuya', 'Teso South', 'Busia'),
#     1112: ('Mukuyuni', 'Teso South', 'Busia'),
#     1113: ('South Bukusu', 'Teso South', 'Busia'),
#     1114: ('Kibingei', 'Nambale', 'Busia'),
#     1115: ('Kimilili', 'Nambale', 'Busia'),
#     1116: ('Maeni', 'Nambale', 'Busia'),
#     1117: ('Kamukuywa', 'Nambale', 'Busia'),
#     1118: ('MALABA CENTRAL', 'Matayos', 'Busia'),
#     1119: ('MALABA NORTH', 'Matayos', 'Busia'),
#     1120: ("ANG'URAI SOUTH", 'Matayos', 'Busia'),
#     1121: ('MALABA SOUTH', 'Matayos', 'Busia'),
#     1122: ("ANG'URAI NORTH", 'Matayos', 'Busia'),
#     1123: ("ANG'URAI EAST", 'Matayos', 'Busia'),
#     1124: ("ANG'OROM", 'Butula', 'Busia'),
#     1125: ('CHAKOI SOUTH', 'Butula', 'Busia'),
#     1126: ('AMUKURA CENTRAL', 'Butula', 'Busia'),
#     1127: ('CHAKOI NORTH', 'Butula', 'Busia'),
#     1128: ('AMUKURA EAST', 'Butula', 'Busia'),
#     1129: ('AMUKURA WEST', 'Butula', 'Busia'),
#     1130: ('NAMBALE TOWNSHIP', 'Funyula', 'Busia'),
#     1131: ('BUKHAYO NORTH/WALTSI', 'Funyula', 'Busia'),
#     1132: ('BUKHAYO EAST', 'Funyula', 'Busia'),
#     1133: ('BUKHAYO CENTRAL', 'Funyula', 'Busia'),
#     1134: ('BUKHAYO WEST', 'Budalangi', 'Busia'),
#     1135: ('MAYENJE', 'Budalangi', 'Busia'),
#     1136: ('MATAYOS SOUTHBUSIBWABO', 'Budalangi', 'Busia'),
#     1137: ('BURUMBA', 'Budalangi', 'Busia'),
#     1138: ('MARACHI WESTKINGANDOLE', 'Ugenya', 'Siaya'),
#     1139: ('MARACHI CENTRAL', 'Ugenya', 'Siaya'),
#     1140: ('MARACHI EAST', 'Ugenya', 'Siaya'),
#     1141: ('MARACHI NORTH', 'Ugenya', 'Siaya'),
#     1142: ('ELUGULU', 'Ugenya', 'Siaya'),
#     1143: ('NAMBOBOTO NAMBUKU', 'Ugunja', 'Siaya'),
#     1144: ('NANGINA', 'Ugunja', 'Siaya'),
#     1145: ("AGENG'A NANGUBA", 'Ugunja', 'Siaya'),
#     1146: ('BWIRI', 'Ugunja', 'Siaya'),
#     1147: ('Usonga', 'Alego Usonga', 'Siaya'),
#     1148: ('West Alego', 'Alego Usonga', 'Siaya'),
#     1149: ('Central Alego', 'Alego Usonga', 'Siaya'),
#     1150: ('Siaya Township', 'Alego Usonga', 'Siaya'),
#     1151: ('North Alego', 'Alego Usonga', 'Siaya'),
#     1152: ('South East Alego', 'Alego Usonga', 'Siaya'),
#     1153: ('North Gem', 'Gem', 'Siaya'),
#     1154: ('West Gem', 'Gem', 'Siaya'),
#     1155: ('Central Gem', 'Gem', 'Siaya'),
#     1156: ('Yala Township', 'Gem', 'Siaya'),
#     1157: ('East Gem', 'Gem', 'Siaya'),
#     1158: ('South Gem', 'Gem', 'Siaya'),
#     1159: ('West Yimbo', 'Bondo', 'Siaya'),
#     1160: ('Central Sakwa', 'Bondo', 'Siaya'),
#     1161: ('South Sakwa', 'Bondo', 'Siaya'),
#     1162: ('Yimbo East', 'Bondo', 'Siaya'),
#     1163: ('West Sakwa', 'Bondo', 'Siaya'),
#     1164: ('North Sakwa', 'Bondo', 'Siaya'),
#     1165: ('Gem Rae', 'Rarieda', 'Siaya'),
#     1166: ('East Asembo', 'Rarieda', 'Siaya'),
#     1167: ('West Asembo', 'Rarieda', 'Siaya'),
#     1168: ('Central Asembo', 'Rarieda', 'Siaya'),
#     1169: ('South West Asembo', 'Rarieda', 'Siaya'),
#     1170: ('North West Asembo', 'Rarieda', 'Siaya'),
#     1171: ('North East Asembo', 'Rarieda', 'Siaya'),
#     1172: ('South East Asembo', 'Rarieda', 'Siaya'),
#     1173: ("Nyang'oma Kogelo", 'Rarieda', 'Siaya'),
#     1174: ('West Uyoma', 'Rarieda', 'Siaya'),
#     1175: ('Central Uyoma', 'Rarieda', 'Siaya'),
#     1176: ('North Uyoma', 'Rarieda', 'Siaya'),
#     1177: ('East Asembo', 'Kisumu East', 'Kisumu'),
#     1178: ('West Asembo', 'Kisumu East', 'Kisumu'),
#     1179: ('North Uyoma', 'Kisumu East', 'Kisumu'),
#     1180: ('South Uyoma', 'Kisumu East', 'Kisumu'),
#     1181: ('West Uyoma', 'Kisumu East', 'Kisumu'),
#     1182: ('Sidindi', 'Kisumu West', 'Kisumu'),
#     1183: ('Sigomere', 'Kisumu West', 'Kisumu'),
#     1184: ('Ugunja', 'Kisumu West', 'Kisumu'),
#     1185: ('Railways', 'Kisumu Central', 'Kisumu'),
#     1186: ('Migosi', 'Kisumu Central', 'Kisumu'),
#     1187: ('Shaurimoyo Kaloleni', 'Kisumu Central', 'Kisumu'),
#     1188: ('Market Milimani', 'Kisumu Central', 'Kisumu'),
#     1189: ('Kondele', 'Kisumu Central', 'Kisumu'),
#     1190: ('Nyalenda B', 'Kisumu Central', 'Kisumu'),
#     1191: ('Kajulu', 'Seme', 'Kisumu'),
#     1192: ('Kolwa East', 'Seme', 'Kisumu'),
#     1193: ("Manyatta 'B'", 'Seme', 'Kisumu'),
#     1194: ("Nyalenda 'A'", 'Seme', 'Kisumu'),
#     1195: ('Kolwa Central', 'Seme', 'Kisumu'),
#     1196: ('South West Kisumu', 'Nyando', 'Kisumu'),
#     1197: ('Cetral Kisumu', 'Nyando', 'Kisumu'),
#     1198: ('Kisumu North', 'Nyando', 'Kisumu'),
#     1199: ('West Kisumu', 'Nyando', 'Kisumu'),
#     1200: ('North West Kisumu', 'Nyando', 'Kisumu'),
#     1201: ('West Seme', 'Muhoroni', 'Kisumu'),
#     1202: ('Central Seme', 'Muhoroni', 'Kisumu'),
#     1203: ('East Seme', 'Muhoroni', 'Kisumu'),
#     1204: ('North Seme', 'Muhoroni', 'Kisumu'),
#     1205: ('East Kano/Waidhi', 'Nyakach', 'Kisumu'),
#     1206: ('Awasi/Onjiko', 'Nyakach', 'Kisumu'),
#     1207: ('Ahero', 'Nyakach', 'Kisumu'),
#     1208: ('Kabonyo/Kanyag Wal', 'Nyakach', 'Kisumu'),
#     1209: ('Kobura', 'Nyakach', 'Kisumu'),
#     1210: ('Miwani', 'Kasipul', 'Homa Bay'),
#     1211: ('Ombeyi', 'Kasipul', 'Homa Bay'),
#     1212: ("Masogo/Nyag'oma", 'Kasipul', 'Homa Bay'),
#     1213: ('Chemeli/Muhoroni/Koru', 'Kasipul', 'Homa Bay'),
#     1214: ('South East Nyakach', 'Kabondo Kasipul', 'Homa Bay'),
#     1215: ('West Nyakach', 'Kabondo Kasipul', 'Homa Bay'),
#     1216: ('North Nyakach', 'Kabondo Kasipul', 'Homa Bay'),
#     1217: ('Central Nyakach', 'Kabondo Kasipul', 'Homa Bay'),
#     1218: ('South West Nyakach', 'Kabondo Kasipul', 'Homa Bay'),
#     1219: ('Homa Bay Central', 'Karachuonyo', 'Homa Bay'),
#     1220: ('Homa Bay Arujo', 'Karachuonyo', 'Homa Bay'),
#     1221: ('Homa Bay West', 'Karachuonyo', 'Homa Bay'),
#     1222: ('Homa Bay East', 'Karachuonyo', 'Homa Bay'),
#     1223: ('Kabondo East', 'Rangwe', 'Homa Bay'),
#     1224: ('Kabondo West', 'Rangwe', 'Homa Bay'),
#     1225: ('Kokwanyo', 'Rangwe', 'Homa Bay'),
#     1226: ('Kakelo-Kojwach', 'Rangwe', 'Homa Bay'),
#     1227: ('West Karachuonyo', 'Homa Bay Town', 'Homa Bay'),
#     1228: ('North Karachuonyo', 'Homa Bay Town', 'Homa Bay'),
#     1229: ('Central Kanyaluo', 'Homa Bay Town', 'Homa Bay'),
#     1230: ('Kibiri', 'Homa Bay Town', 'Homa Bay'),
#     1231: ('Wangchieng', 'Homa Bay Town', 'Homa Bay'),
#     1232: ('Kendu Bay Town', 'Homa Bay Town', 'Homa Bay'),
#     1233: ('West Kasipul', 'Ndhiwa', 'Homa Bay'),
#     1234: ('South Kasipul', 'Ndhiwa', 'Homa Bay'),
#     1235: ('Central Kasipul', 'Ndhiwa', 'Homa Bay'),
#     1236: ('East Kamagak', 'Ndhiwa', 'Homa Bay'),
#     1237: ('West Kamagak', 'Ndhiwa', 'Homa Bay'),
#     1238: ('Kwabwai', 'Mbita', 'Homa Bay'),
#     1239: ('Kanyadoto', 'Mbita', 'Homa Bay'),
#     1240: ('Kanyikela', 'Mbita', 'Homa Bay'),
#     1241: ('Kabuoch North', 'Mbita', 'Homa Bay'),
#     1242: ('Kabuoch South/Pala', 'Mbita', 'Homa Bay'),
#     1243: ('Kanyamwa Kologi', 'Mbita', 'Homa Bay'),
#     1244: ('Kanyamwa Kosewe', 'Mbita', 'Homa Bay'),
#     1245: ('West Gem', 'Suba', 'Homa Bay'),
#     1246: ('East Gem', 'Suba', 'Homa Bay'),
#     1247: ('Kagan', 'Suba', 'Homa Bay'),
#     1248: ('Kochia', 'Suba', 'Homa Bay'),
#     1249: ('Mfangano Island', 'Rongo', 'Migori'),
#     1250: ('Rusinga Island', 'Rongo', 'Migori'),
#     1251: ('Kasgunga', 'Rongo', 'Migori'),
#     1252: ('Gember', 'Rongo', 'Migori'),
#     1253: ('Lambwe', 'Rongo', 'Migori'),
#     1254: ('Gwassi South', 'Awendo', 'Migori'),
#     1255: ('Gwassi North', 'Awendo', 'Migori'),
#     1256: ('Kaksingri West', 'Awendo', 'Migori'),
#     1257: ('Ruma-Kakshingri', 'Awendo', 'Migori'),
#     1258: ('North Kamagambo', 'Suna East', 'Migori'),
#     1259: ('Central Kamagambo', 'Suna East', 'Migori'),
#     1260: ('East Kamagambo', 'Suna East', 'Migori'),
#     1261: ('South Kamagambo', 'Suna East', 'Migori'),
#     1262: ('North East Sakwa', 'Suna West', 'Migori'),
#     1263: ('South Sakwa', 'Suna West', 'Migori'),
#     1264: ('West Sakwa', 'Suna West', 'Migori'),
#     1265: ('Central Sakwa', 'Suna West', 'Migori'),
#     1266: ('God Jope', 'Uriri', 'Migori'),
#     1267: ('Suna Central', 'Uriri', 'Migori'),
#     1268: ('Kakrao', 'Uriri', 'Migori'),
#     1269: ('Kwa', 'Uriri', 'Migori'),
#     1270: ('Wiga', 'Nyatike', 'Migori'),
#     1271: ('Wasweta II', 'Nyatike', 'Migori'),
#     1272: ('Ragan-Oruba', 'Nyatike', 'Migori'),
#     1273: ('Wasimbete', 'Nyatike', 'Migori'),
#     1274: ('West Kanyamkago', 'Kuria West', 'Migori'),
#     1275: ('North Kanyamkago', 'Kuria West', 'Migori'),
#     1276: ('Central Kanyam Kago', 'Kuria West', 'Migori'),
#     1277: ('South Kanyamkago', 'Kuria West', 'Migori'),
#     1278: ('East Kanyamkago', 'Kuria West', 'Migori'),
#     1279: ('Kachieng', 'Kuria East', 'Migori'),
#     1280: ('Kanyasa', 'Kuria East', 'Migori'),
#     1281: ('North Kadem', 'Kuria East', 'Migori'),
#     1282: ('Macalder/ Kanyarwanda', 'Kuria East', 'Migori'),
#     1283: ('Kaler', 'Kuria East', 'Migori'),
#     1284: ('Got Kachola', 'Kuria East', 'Migori'),
#     1285: ('Muhuru', 'Kuria East', 'Migori'),
#     1286: ('Gokeharaka/Getamwega', 'Bonchari', 'Kisii'),
#     1287: ('Ntimaru West', 'Bonchari', 'Kisii'),
#     1288: ('Ntimaru East', 'Bonchari', 'Kisii'),
#     1289: ('Nyabasi East', 'Bonchari', 'Kisii'),
#     1290: ('Nyabasi West', 'Bonchari', 'Kisii'),
#     1291: ('Bukira East', 'South Mugirango', 'Kisii'),
#     1292: ('Bukira Central/ Ikerege', 'South Mugirango', 'Kisii'),
#     1293: ('Isibania', 'South Mugirango', 'Kisii'),
#     1294: ('Makerero', 'South Mugirango', 'Kisii'),
#     1295: ('Masaba', 'South Mugirango', 'Kisii'),
#     1296: ('Tagare', 'South Mugirango', 'Kisii'),
#     1297: ('Nyamosense/Ko Mosoko', 'South Mugirango', 'Kisii'),
#     1298: ('MONYERERO', 'Bomachoge Borabu', 'Kisii'),
#     1299: ('SENSI', 'Bomachoge Borabu', 'Kisii'),
#     1300: ('MARANI', 'Bomachoge Borabu', 'Kisii'),
#     1301: ('MWAMONARI', 'Bomachoge Borabu', 'Kisii'),
#     1302: ('BOGUSERO', 'Bobasi', 'Kisii'),
#     1303: ('BOGEKA', 'Bobasi', 'Kisii'),
#     1304: ('NYAKOE', 'Bobasi', 'Kisii'),
#     1305: ('KITUTU CENTRAL', 'Bobasi', 'Kisii'),
#     1306: ('NYATIEKO', 'Bobasi', 'Kisii'),
#     1307: ('ICHUNI', 'Bomachoge Chache', 'Kisii'),
#     1308: ('NYAMASIBI', 'Bomachoge Chache', 'Kisii'),
#     1309: ('MASIMBA', 'Bomachoge Chache', 'Kisii'),
#     1310: ('GESUSU', 'Bomachoge Chache', 'Kisii'),
#     1311: ('KIAMOKAMA', 'Bomachoge Chache', 'Kisii'),
#     1312: ('BOBARACHO', 'Nyaribari Masaba', 'Kisii'),
#     1313: ('KISII CENTRAL', 'Nyaribari Masaba', 'Kisii'),
#     1314: ('KEUMBU', 'Nyaribari Masaba', 'Kisii'),
#     1315: ('KIOGORO', 'Nyaribari Masaba', 'Kisii'),
#     1316: ('BIRONGO', 'Nyaribari Masaba', 'Kisii'),
#     1317: ('IBENO', 'Nyaribari Masaba', 'Kisii'),
#     1318: ('BORABU MASABA', 'Nyaribari Chache', 'Kisii'),
#     1319: ('BOOCHI BORABU', 'Nyaribari Chache', 'Kisii'),
#     1320: ('BOKIMONGE', 'Nyaribari Chache', 'Kisii'),
#     1321: ('MAGENCHE', 'Nyaribari Chache', 'Kisii'),
#     1322: ('MAJOGE BASI', 'Kitutu Chache North', 'Kisii'),
#     1323: ('BOOCHI/TENDERE', 'Kitutu Chache North', 'Kisii'),
#     1324: ('BOSOTI/SENGERA', 'Kitutu Chache North', 'Kisii'),
#     1325: ('MASIGE WEST', 'Kitutu Chache South', 'Kisii'),
#     1326: ('MASIG EAST', 'Kitutu Chache South', 'Kisii'),
#     1327: ('BASI CENTRAL', 'Kitutu Chache South', 'Kisii'),
#     1328: ('NYACHEKI', 'Kitutu Chache South', 'Kisii'),
#     1329: ('BASSI BOGETAORIO', 'Kitutu Chache South', 'Kisii'),
#     1330: ('BOBASI CHACHE', 'Kitutu Chache South', 'Kisii'),
#     1331: ('SAMETA/ MOKWERERO', 'Kitutu Chache South', 'Kisii'),
#     1332: ('BOBASI/ BOITANGARE', 'Kitutu Chache South', 'Kisii'),
#     1333: ('BOGETENGA', 'Kitutu Masaba', 'Nyamira'),
#     1334: ('BORABU/CHITAGO', 'Kitutu Masaba', 'Nyamira'),
#     1335: ('MOTICHO', 'Kitutu Masaba', 'Nyamira'),
#     1336: ('GETENGA', 'Kitutu Masaba', 'Nyamira'),
#     1337: ('TABAKA', 'Kitutu Masaba', 'Nyamira'),
#     1338: ('BOIKANGA', 'Kitutu Masaba', 'Nyamira'),
#     1339: ('BOMARIBA', 'West Mugirango', 'Nyamira'),
#     1340: ('BOGIAKUMU', 'West Mugirango', 'Nyamira'),
#     1341: ('BOKEIRA', 'West Mugirango', 'Nyamira'),
#     1342: ('RIANA', 'West Mugirango', 'Nyamira'),
#     1343: ('Mekenene', 'North Mugirango', 'Nyamira'),
#     1344: ('Kiabonyoru', 'North Mugirango', 'Nyamira'),
#     1345: ('Esise', 'North Mugirango', 'Nyamira'),
#     1346: ('Nyansiongo', 'North Mugirango', 'Nyamira'),
#     1347: ('Rigoma', 'Borabu', 'Nyamira'),
#     1348: ('Gachuba', 'Borabu', 'Nyamira'),
#     1349: ('Kemera', 'Borabu', 'Nyamira'),
#     1350: ('Magombo', 'Borabu', 'Nyamira'),
#     1351: ('Manga', 'Borabu', 'Nyamira'),
#     1352: ('Gesima', 'Borabu', 'Nyamira'),
#     1353: ('Nyamaiya', 'Westlands', 'Nairobi City'),
#     1354: ('Bogichora', 'Westlands', 'Nairobi City'),
#     1355: ('Bosamaro', 'Westlands', 'Nairobi City'),
#     1356: ('Bonyamatuta', 'Westlands', 'Nairobi City'),
#     1357: ('Township', 'Westlands', 'Nairobi City'),
#     1358: ('Itibo', 'Dagoretti North', 'Nairobi City'),
#     1359: ('Bomwagamo', 'Dagoretti North', 'Nairobi City'),
#     1360: ('Bokeira', 'Dagoretti North', 'Nairobi City'),
#     1361: ('Magwagwa', 'Dagoretti North', 'Nairobi City'),
#     1362: ('Ekerenyo', 'Dagoretti North', 'Nairobi City'),
#     1363: ('Kitisuru', 'Dagoretti South', 'Nairobi City'),
#     1364: ('Parklands/Highridge', 'Dagoretti South', 'Nairobi City'),
#     1365: ('Karura', 'Dagoretti South', 'Nairobi City'),
#     1366: ('Kangemi', 'Dagoretti South', 'Nairobi City'),
#     1367: ('Mountain View', 'Dagoretti South', 'Nairobi City'),
#     1368: ('Kilimani', "Lang'ata", 'Nairobi City'),
#     1369: ('Kawangware', "Lang'ata", 'Nairobi City'),
#     1370: ('Gatina', "Lang'ata", 'Nairobi City'),
#     1371: ('Kileleshwa', "Lang'ata", 'Nairobi City'),
#     1372: ('Kabiro', "Lang'ata", 'Nairobi City'),
#     1373: ('Mutu-Ini', 'Kibra', 'Nairobi City'),
#     1374: ('Ngando', 'Kibra', 'Nairobi City'),
#     1375: ('Riruta', 'Kibra', 'Nairobi City'),
#     1376: ('Uthiru/Ruthimitu', 'Kibra', 'Nairobi City'),
#     1377: ('Waithaka', 'Kibra', 'Nairobi City'),
#     1378: ('Karen', 'Roysambu', 'Nairobi City'),
#     1379: ('Nairobi West', 'Roysambu', 'Nairobi City'),
#     1380: ('Mugumu-Ini', 'Roysambu', 'Nairobi City'),
#     1381: ('South C', 'Roysambu', 'Nairobi City'),
#     1382: ('Nyayo Highrise', 'Roysambu', 'Nairobi City'),
#     1383: ('Woodley/Kenyatta Golf Course', 'Kasarani', 'Nairobi City'),
#     1384: ("Sarang'ombe", 'Kasarani', 'Nairobi City'),
#     1385: ('Makina', 'Kasarani', 'Nairobi City'),
#     1386: ('Lindi', 'Kasarani', 'Nairobi City'),
#     1387: ('Laini Saba', 'Kasarani', 'Nairobi City'),
#     1388: ('Kahawa West', 'Ruaraka', 'Nairobi City'),
#     1389: ('Roysambu', 'Ruaraka', 'Nairobi City'),
#     1390: ('Githurai', 'Ruaraka', 'Nairobi City'),
#     1391: ('Kahawa', 'Ruaraka', 'Nairobi City'),
#     1392: ('Zimmerman', 'Ruaraka', 'Nairobi City'),
#     1393: ('Kasarani', 'Embakasi South', 'Nairobi City'),
#     1394: ('Njiru', 'Embakasi South', 'Nairobi City'),
#     1395: ('Clay City', 'Embakasi South', 'Nairobi City'),
#     1396: ('Mwiki', 'Embakasi South', 'Nairobi City'),
#     1397: ('Ruai', 'Embakasi South', 'Nairobi City'),
#     1398: ('Utalii', 'Embakasi North', 'Nairobi City'),
#     1399: ('Korogocho', 'Embakasi North', 'Nairobi City'),
#     1400: ('Lucky Summer', 'Embakasi North', 'Nairobi City'),
#     1401: ('Mathare North', 'Embakasi North', 'Nairobi City'),
#     1402: ('Baba Dogo', 'Embakasi North', 'Nairobi City'),
#     1403: ('Kwa Njenga', 'Embakasi Central', 'Nairobi City'),
#     1404: ('Imara Daima', 'Embakasi Central', 'Nairobi City'),
#     1405: ('Kware', 'Embakasi Central', 'Nairobi City'),
#     1406: ('Kwa Reuben', 'Embakasi Central', 'Nairobi City'),
#     1407: ('Pipeline', 'Embakasi Central', 'Nairobi City'),
#     1408: ('Dandora Area I', 'Embakasi East', 'Nairobi City'),
#     1409: ('Dandora Area II', 'Embakasi East', 'Nairobi City'),
#     1410: ('Dandora Area III', 'Embakasi East', 'Nairobi City'),
#     1411: ('Dandora Area IV', 'Embakasi East', 'Nairobi City'),
#     1412: ('Kariobangi North', 'Embakasi East', 'Nairobi City'),
#     1413: ('Kayole North', 'Embakasi West', 'Nairobi City'),
#     1414: ('Kayole Central', 'Embakasi West', 'Nairobi City'),
#     1415: ('Kariobangi South', 'Embakasi West', 'Nairobi City'),
#     1416: ('Komarock', 'Embakasi West', 'Nairobi City'),
#     1417: ('Matopeni / Spring Valley', 'Embakasi West', 'Nairobi City'),
#     1418: ('Utawala', 'Makadara', 'Nairobi City'),
#     1419: ('Upper Savanna', 'Makadara', 'Nairobi City'),
#     1420: ('Lower Savanna', 'Makadara', 'Nairobi City'),
#     1421: ('Embakasi', 'Makadara', 'Nairobi City'),
#     1422: ('Mihango', 'Makadara', 'Nairobi City'),
#     1423: ('Umoja 1', 'Kamukunji', 'Nairobi City'),
#     1424: ('Umoja 2', 'Kamukunji', 'Nairobi City'),
#     1425: ('Mowlem', 'Kamukunji', 'Nairobi City'),
#     1426: ('Kariobangi south', 'Kamukunji', 'Nairobi City'),
#     1427: ('Maringo/ Hamza', 'Kamukunji', 'Nairobi City'),
#     1428: ('Viwandani', 'Starehe', 'Nairobi City'),
#     1429: ('Harambee', 'Starehe', 'Nairobi City'),
#     1430: ('Makongeni', 'Starehe', 'Nairobi City'),
#     1431: ('Pumwani', 'Starehe', 'Nairobi City'),
#     1432: ('Eastleigh North', 'Starehe', 'Nairobi City'),
#     1433: ('Eastleigh South', 'Mathare', 'Nairobi City'),
#     1434: ('Nairobi Central', 'Mathare', 'Nairobi City'),
#     1435: ('Airbase', 'Mathare', 'Nairobi City'),
#     1436: ('California', 'Mathare', 'Nairobi City'),
#     1437: ('Mgara', 'Mathare', 'Nairobi City'),
#     1438: ('Nairobi South', 'Mathare', 'Nairobi City'),
#     1439: ('Hospital', 'Mathare', 'Nairobi City'),
#     1440: ('Ngara', 'Mathare', 'Nairobi City'),
#     1441: ('Pangani', 'Mathare', 'Nairobi City'),
#     1442: ('Landimawe', 'Mathare', 'Nairobi City'),
#     1443: ('Ziwani / Kariokor', 'Mathare', 'Nairobi City'),
#     1444: ('Mlango Kubwa', 'Mathare', 'Nairobi City'),
#     1445: ('Kiamaiko', 'Mathare', 'Nairobi City'),
#     1446: ('Ngei', 'Mathare', 'Nairobi City'),
#     1447: ('Huruma', 'Mathare', 'Nairobi City'),
#     1448: ('Mabatini', 'Mathare', 'Nairobi City'),
# }


# ============================================================
# Replace get_candidates in views.py with this:
# ============================================================


import random
import string
from django.contrib.auth.hashers import make_password, check_password

@api_view(['GET'])
def index (request): 
        return Response("Hello Timo")
    
@api_view(['POST'])
@csrf_exempt
def signup (request):
    if request.method == "POST":  
        print(request.data)
        
        id_number = request.data.get("id_number", "").strip()
        phone_number = request.data.get("phone", "").strip()
        
        # Check if ID or Phone already exists
        if Voter.objects.filter(id_number=id_number).exists():
            return Response({"id_number": ["A voter with this ID number is already registered."]}, status=400)
        
        if Voter.objects.filter(phone_number=phone_number).exists():
            return Response({"phone": ["A voter with this phone number is already registered."]}, status=400)
            
        generated_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        hashed_password = make_password(generated_code)
        
        try:
            user = Voter.objects.create(
                full_name=request.data.get("full_name").strip(),
                phone_number=phone_number,
                constituency=request.data.get("constituency"),
                county=request.data.get("county"),
                ward=request.data.get("ward"),
                id_number=id_number,
                email = request.data.get("email"),
                voter_code=generated_code,
                password_hash=hashed_password
            )
    
            user.save()
            import smtplib
            import threading
            
            def send_registration_email(user, code):
                try:
                    send_mail(
                        subject='Your Uchaguzi Voter Code',
                        message=f'Hello {user.full_name},\n\nYour voter code is: {code}\n\nUse this code along with your ID number to log in and vote. You will be prompted to change your password upon your first login.\n\nuChaguzi Electoral System',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email, 'muokijr@gmail.com'],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Failed to send email to {user.email}: {e}")

            # Send email in background to prevent slow registration spinning
            threading.Thread(target=send_registration_email, args=(user, generated_code)).start()

            return Response({"message":"Registration successful", "voter_code": generated_code}, status=200)
        except IntegrityError:
            return Response({"message":"User already exists"}, status=400)
    return Response({"message":"signup"}, status=200)


# @api_view(["POST"])
# def login(request):
#     if request.method == "POST":
#         print(request.data)
#         return Response({"message":"login"}, status=200)

@api_view(["POST"])
@csrf_exempt
def login(request):
    id_number = request.data.get("id_number", "").strip()
    password = request.data.get("voter_code", "").strip()

    if not id_number or not password:
        return Response({"message": "ID number and password are required"}, status=400)

    try:
        voter = Voter.objects.get(id_number=id_number)
    except Voter.DoesNotExist:
        return Response({"message": "Invalid credentials"}, status=401)

    if not check_password(password, voter.password_hash):
        return Response({"message": "Invalid credentials"}, status=401)

    requires_password_change = check_password(voter.voter_code, voter.password_hash)

    voted_seats = Vote.objects.filter(voter=voter).values_list('seat__seat_type', flat=True)

    return Response({
        "message": "Login successful",
        "requires_password_change": requires_password_change,
        "user": {
            "id": voter.id,
            "full_name": voter.full_name,
            "voter_code": str(voter.voter_code),
            "id_number": voter.id_number,
            "county": voter.county,
            "constituency": voter.constituency,
            "ward": voter.ward,
            "has_voted": list(voted_seats)
        }
    }, status=200)

import re

@api_view(["POST"])
@csrf_exempt
def change_password(request):
    id_number = request.data.get("id_number", "").strip()
    old_password = request.data.get("old_password", "").strip()
    new_password = request.data.get("new_password", "").strip()

    if not all([id_number, old_password, new_password]):
        return Response({"message": "All fields are required"}, status=400)

    try:
        voter = Voter.objects.get(id_number=id_number)
    except Voter.DoesNotExist:
        return Response({"message": "Voter not found"}, status=404)

    if not check_password(old_password, voter.password_hash):
        return Response({"message": "Invalid current password"}, status=401)

    if len(new_password) < 8 or len(new_password) > 16:
        return Response({"message": "Password must be between 8 and 16 characters"}, status=400)
    
    if not re.search(r"[A-Z]", new_password):
        return Response({"message": "Password must contain an uppercase letter"}, status=400)
        
    if not re.search(r"[a-z]", new_password):
        return Response({"message": "Password must contain a lowercase letter"}, status=400)
        
    if not re.search(r"\d", new_password):
        return Response({"message": "Password must contain a number"}, status=400)
        
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
        return Response({"message": "Password must contain a special character"}, status=400)

    voter.password_hash = make_password(new_password)
    voter.save()

    return Response({"message": "Password changed successfully"}, status=200)
    
#vote api

@api_view(["POST"])
@csrf_exempt
def cast_vote(request):
    print("DATA RECEIVED:", request.data)
    try:
        voter_id = int(request.data.get("voter_id"))
        seat_id = int(request.data.get("seat_id"))
        candidate_id = int(request.data.get("candidate_id"))
        print(f"IDs: voter={voter_id}, seat={seat_id}, candidate={candidate_id}")
    except (TypeError, ValueError) as e:
        print("CONVERSION ERROR:", e)
        return Response({"message": "Invalid ID format"}, status=400)

    try:
        voter = Voter.objects.get(id=voter_id)
        print("Voter found:", voter)
    except Voter.DoesNotExist:
        print("Voter NOT found")
        return Response({"message": "Voter not found"}, status=404)

    try:
        seat = Seat.objects.get(id=seat_id)
        print("Seat found:", seat)
    except Seat.DoesNotExist:
        print("Seat NOT found")
        return Response({"message": "Seat not found"}, status=404)

    try:
        candidate = Candidate.objects.get(id=candidate_id)
        print("Candidate found:", candidate)
    except Candidate.DoesNotExist:
        print("Candidate NOT found")
        return Response({"message": "Candidate not found"}, status=404)

    try:
        from django.db import transaction
        with transaction.atomic():
            Vote.objects.create(voter=voter, seat=seat, candidate=candidate)
        return Response({"message": "Vote cast successfully"}, status=200)
    except IntegrityError:
        return Response({"message": "You have already voted for this seat"}, status=400)
    
from django.db.models import Q

KENYA_COUNTIES = {
    1: 'Mombasa', 2: 'Kwale', 3: 'Kilifi', 4: 'Tana River', 5: 'Lamu', 6: 'Taita-Taveta', 
    7: 'Garissa', 8: 'Wajir', 9: 'Mandera', 10: 'Marsabit', 11: 'Isiolo', 12: 'Meru', 
    13: 'Tharaka-Nithi', 14: 'Embu', 15: 'Kitui', 16: 'Machakos', 17: 'Makueni', 
    18: 'Nyandarua', 19: 'Nyeri', 20: 'Kirinyaga', 21: 'Murang\'a', 22: 'Kiambu', 
    23: 'Turkana', 24: 'West Pokot', 25: 'Samburu', 26: 'Trans-Nzoia', 27: 'Uasin Gishu', 
    28: 'Elgeyo-Marakwet', 29: 'Nandi', 30: 'Baringo', 31: 'Laikipia', 32: 'Nakuru', 
    33: 'Narok', 34: 'Kajiado', 35: 'Kericho', 36: 'Bomet', 37: 'Kakamega', 38: 'Vihiga', 
    39: 'Bungoma', 40: 'Busia', 41: 'Siaya', 42: 'Kisumu', 43: 'Homa Bay', 44: 'Migori', 
    45: 'Kisii', 46: 'Nyamira', 47: 'Nairobi'
}

def get_formatted_seat_name(seat):
    if seat.level == 'County' and seat.county:
        county_name = KENYA_COUNTIES.get(int(seat.county), f"County {seat.county}")
        return f"{seat.seat_type} for {county_name} County"
    return seat.name

@api_view(["GET"])
def get_candidates(request):
    county = request.GET.get("county")
    constituency = request.GET.get("constituency")
    ward = request.GET.get("ward")
    seat_type = request.GET.get("seat_type")

    # Filter seats effectively from the DB directly without loading all records into memory
    db_filter = Q(level='National')
    if county:
        db_filter |= Q(level='County', county=county)
    if constituency:
        db_filter |= Q(level='Constituency', constituency=constituency)
    if ward:
        db_filter |= Q(level='Ward', ward=ward)
        
    seats = Seat.objects.filter(db_filter).prefetch_related('candidates')
    
    if seat_type:
        seats = seats.filter(seat_type=seat_type)
        
    result = []
    for seat in seats:
        candidates = seat.candidates.all()
        if candidates:
            result.append({
                "seat_id": seat.id,
                "seat_type": seat.seat_type,
                "seat_name": get_formatted_seat_name(seat),
                "candidates": [{"id": c.id, "full_name": c.full_name, "party": c.party} for c in candidates]
            })

    return Response(result, status=200)



from django.db.models import Count

@api_view(["GET"])
def get_results(request):
    """
    Returns aggregated vote counts grouped by seat. Accepts optional area-based filtering.
    """
    county = request.query_params.get("county")
    constituency = request.query_params.get("constituency")
    ward = request.query_params.get("ward")
    seat_type = request.query_params.get("seat_type")

    db_filter = models.Q(level='National')
    if county:
        db_filter |= models.Q(level='County', county=county)
    if constituency:
        db_filter |= models.Q(level='Constituency', constituency=constituency)
    if ward:
        db_filter |= models.Q(level='Ward', ward=ward)

    from django.db.models import Count, Prefetch

    candidate_qs = Candidate.objects.annotate(vote_count=Count('votes'))
    seats = Seat.objects.filter(db_filter).prefetch_related(Prefetch('candidates', queryset=candidate_qs))
    if seat_type:
        seats = seats.filter(seat_type=seat_type)

    result = []
    for seat in seats:
        candidates = seat.candidates.all()
        
        if candidates:
            result.append({
                "seat_id": seat.id,
                "seat_type": seat.seat_type,
                "seat_name": get_formatted_seat_name(seat),
                "results": [
                    {
                        "candidate_id": c.id,
                        "full_name": c.full_name,
                        "party": c.party,
                        "votes": c.vote_count
                    }
                    for c in candidates
                ]
            })

    return Response(result, status=200)


@api_view(["GET"])
def voter_status(request):
    voter_id = request.query_params.get('voter_id')
    if not voter_id:
        return Response({"error": "voter_id required"}, status=400)

    try:
        voter = Voter.objects.get(id=voter_id)
    except Voter.DoesNotExist:
        return Response({"message": "Voter not found"}, status=404)

    voted_seats = Vote.objects.filter(voter=voter).values_list('seat__seat_type', flat=True)
    return Response({"has_voted": list(voted_seats)}, status=200)
    

import google.generativeai as genai
import os

# Try to get key from environment, fallback to a dummy if not set (will fail gracefully)
api_key = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)

@api_view(["POST"])
@csrf_exempt
def summarize_candidate(request):
    try:
        candidate_id = request.data.get("candidate_id")
        if not candidate_id:
            return Response({"error": "candidate_id is required"}, status=400)
            
        candidate = Candidate.objects.select_related('seat').get(id=candidate_id)
        
        prompt = f"""
        You are an impartial election guide for the Kenyan 'Uchaguzi' digital voting system. 
        Write a very concise, neutral 2-sentence summary introducing the following candidate.
        Name: {candidate.full_name}
        Party: {candidate.party}
        Running for: {get_formatted_seat_name(candidate.seat)} ({candidate.seat.seat_type})
        Manifesto Details: {candidate.manifesto or ''}
        
        Instructions:
        1. If '{candidate.full_name}' is a universally known, real-world political figure (e.g., a real Kenyan Presidential candidate like William Ruto or Raila Odinga), DO NOT output a generic summary. Instead, use your extensive real-world knowledge to neutrally summarize their actual historical political platform, their current agenda, and what they are famous for.
        2. If '{candidate.full_name}' is a fictional or unknown local name, do not invent facts. Just summarize what a candidate in the role of {candidate.seat.name} generally aims to achieve for their constituents.
        """
        
        # Use standard gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        return Response({"summary": response.text.strip()}, status=200)
        
    except Candidate.DoesNotExist:
        return Response({"error": "Candidate not found"}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": f"AI Generation failed: {str(e)}"}, status=500)


@api_view(["POST"])
@csrf_exempt
def admin_login(request):
    key = request.data.get("admin_key", "")
    if key == "IEBC2026": # Master key
        return Response({"message": "Authorized", "token": "admin-token-777"}, status=200)
    return Response({"message": "Unauthorized"}, status=401)

@api_view(["GET"])
def admin_stats(request):
    import os
    total_voters = Voter.objects.count()
    total_votes = Vote.objects.count()
    active_voters = Vote.objects.values('voter').distinct().count()
    total_candidates = Candidate.objects.count()

    return Response({
        "total_voters": total_voters,
        "total_votes": total_votes,
        "active_voters": active_voters,
        "total_candidates": total_candidates,
        "velocity": total_votes // 10 if total_votes > 0 else 0,
        "is_active": not os.path.exists("HALT_ELECTION.flag")
    }, status=200)

@api_view(["GET"])
def admin_voters(request):
    voters = Voter.objects.values('id', 'voter_code', 'full_name', 'county', 'constituency', 'ward', 'created_at', 'password_hash').order_by('-created_at')[:50]
    return Response(list(voters), status=200)

@api_view(["GET"])
def admin_candidates(request):
    candidates = Candidate.objects.select_related('seat').all().order_by('seat__seat_type', 'full_name')[:2000]
    data = [{
        'id': c.id,
        'full_name': c.full_name,
        'party': c.party,
        'seat_name': c.seat.name,
        'seat_level': c.seat.level,
        'seat_type': c.seat.seat_type
    } for c in candidates]
    return Response(data, status=200)

@api_view(["GET"])
def admin_votes(request):
    votes = Vote.objects.select_related('voter', 'seat', 'candidate').order_by('-voted_at')[:50]
    data = [{
        'id': v.id,
        'voter_code': v.voter.voter_code,
        'voter_name': v.voter.full_name,
        'seat': v.seat.name,
        'candidate': v.candidate.full_name,
        'time': v.voted_at
    } for v in votes]
    return Response(data, status=200)

@api_view(["POST"])
def admin_toggle_halt(request):
    import os
    flag_path = "HALT_ELECTION.flag"
    if os.path.exists(flag_path):
        os.remove(flag_path)
        is_active = True
    else:
        with open(flag_path, 'w') as f:
            f.write("HALTED")
        is_active = False
    return Response({"is_active": is_active}, status=200)

@api_view(["POST"])
def admin_candidate_add(request):
    seat_type = request.data.get('seat_type', 'president')
    region_name = request.data.get('region_name', '').strip()
    
    if seat_type in ['governor', 'senator', 'woman_rep'] and region_name:
        seat = Seat.objects.filter(seat_type=seat_type, county__iexact=region_name).first()
    elif seat_type == 'mp' and region_name:
        seat = Seat.objects.filter(seat_type=seat_type, constituency__iexact=region_name).first()
    elif seat_type == 'mca' and region_name:
        seat = Seat.objects.filter(seat_type=seat_type, ward__iexact=region_name).first()
    else:
        seat = Seat.objects.filter(seat_type=seat_type).first()

    if not seat:
         return Response({"error": f"No matching seat available for {seat_type} in '{region_name}'"}, status=400)
    
    Candidate.objects.create(
         full_name=request.data.get('full_name'),
         party=request.data.get('party', 'Independent'),
         seat=seat
    )
    return Response({"message": "Successfully added candidate"}, status=201)

@api_view(["DELETE"])
def admin_candidate_delete(request, id):
    try:
        Candidate.objects.get(id=id).delete()
        return Response({"message": "Successfully deleted candidate and their votes"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["DELETE"])
def admin_voter_delete(request, id):
    try:
        Voter.objects.get(id=id).delete()
        return Response({"message": "Successfully deleted voter"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["DELETE"])
def admin_voter_delete_all(request):
    try:
        Voter.objects.all().delete()
        return Response({"message": "Successfully deleted all voters"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def admin_voter_reset_password(request, id):
    try:
        voter = Voter.objects.get(id=id)
        # Reset to temporary code (voter_code)
        voter.password_hash = make_password(voter.voter_code)
        voter.save()
        return Response({"message": "Password reset successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

from django.core.management import call_command
from io import StringIO

@api_view(['POST'])
@csrf_exempt
def force_load_candidates(request):
    key = request.data.get("admin_key", "")
    if key != "IEBC2026":
        return Response({"error": "Unauthorized"}, status=401)
        
    out = StringIO()
    err = StringIO()
    try:
        # Use absolute path if possible or relative to BASE_DIR
        csv_path = os.path.join(settings.BASE_DIR, 'test_candidates.csv')
        call_command('load_candidates', csv_path, force=True, stdout=out, stderr=err)
        return Response({
            "stdout": out.getvalue(),
            "stderr": err.getvalue()
        })
    except Exception as e:
        return Response({
            "error": str(e),
            "stdout": out.getvalue(),
            "stderr": err.getvalue()
        }, status=500)
def admin_candidate_delete_all(request):
    try:
        Candidate.objects.all().delete()
        return Response({"message": "Successfully deleted all candidates and their votes"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["DELETE"])
def admin_voter_delete(request, id):
    try:
        Voter.objects.get(id=id).delete()
        return Response({"message": "Successfully deleted voter and their votes"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["DELETE"])
def admin_voter_delete_all(request):
    try:
        Voter.objects.all().delete()
        return Response({"message": "Successfully deleted all voters and their votes"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def admin_voter_reset_password(request, id):
    try:
        voter = Voter.objects.get(id=id)
        voter.password_hash = make_password("IEBC2026!")
        voter.save()
        return Response({"message": f"Password for {voter.full_name} reset to 'IEBC2026!'"}, status=200)
    except Voter.DoesNotExist:
        return Response({"error": "Voter not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def admin_restart_election(request):
    try:
        Vote.objects.all().delete()
        return Response({"message": "All votes absolutely wiped. Election restarted."}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

from django.db.models import Count

@api_view(["GET"])
def get_all_leaders(request):
    seats = Seat.objects.all()
    results = []
    for seat in seats:
        leader = Vote.objects.filter(seat=seat).values(
            'candidate__full_name', 'candidate__party'
        ).annotate(votes=Count('id')).order_by('-votes').first()
        
        if leader:
            results.append({
                'seat_name': seat.name,
                'seat_type': seat.seat_type,
                'level': seat.level,
                'leader_name': leader['candidate__full_name'],
                'leader_party': leader['candidate__party'],
                'votes': leader['votes']
            })
    return Response(results, status=200)

@api_view(["GET"])
def get_ward_analysis(request, ward_id):
    # How did voters in this ward vote?
    votes = Vote.objects.filter(voter__ward=ward_id).values(
        'seat__seat_type', 'candidate__full_name', 'candidate__party'
    ).annotate(votes=Count('id')).order_by('seat__seat_type', '-votes')
    
    analysis = {}
    for v in votes:
        stype = v['seat__seat_type']
        if stype not in analysis:
            analysis[stype] = []
        analysis[stype].append({
            'candidate': v['candidate__full_name'],
            'party': v['candidate__party'],
            'votes': v['votes']
        })
    return Response(analysis, status=200)

@api_view(["GET"])
def get_constituency_analysis(request, constituency_id):
    # How did voters in this constituency vote?
    votes = Vote.objects.filter(voter__constituency=constituency_id).values(
        'seat__seat_type', 'candidate__full_name', 'candidate__party'
    ).annotate(votes=Count('id')).order_by('seat__seat_type', '-votes')
    
    analysis = {}
    for v in votes:
        stype = v['seat__seat_type']
        if stype not in analysis:
            analysis[stype] = []
        analysis[stype].append({
            'candidate': v['candidate__full_name'],
            'party': v['candidate__party'],
            'votes': v['votes']
        })
    return Response(analysis, status=200)

PROVINCE_TO_COUNTY = {
    'Coast': list(range(1, 7)),
    'North Eastern': list(range(7, 10)),
    'Eastern': list(range(10, 18)),
    'Central': list(range(18, 23)),
    'Rift Valley': list(range(23, 37)),
    'Western': list(range(37, 41)),
    'Nyanza': list(range(41, 47)),
    'Nairobi': [47],
}

@api_view(["GET"])
def get_all_candidates_analysis(request):
    province = request.query_params.get('province')
    county_id = request.query_params.get('county')
    constituency_id = request.query_params.get('constituency')
    
    # Base query for all votes
    votes_query = Vote.objects.all()
    
    # Apply filters based on the voter's location
    if constituency_id:
        votes_query = votes_query.filter(voter__constituency=constituency_id)
    elif county_id:
        votes_query = votes_query.filter(voter__county=county_id)
    elif province and province in PROVINCE_TO_COUNTY:
        counties = PROVINCE_TO_COUNTY[province]
        votes_query = votes_query.filter(voter__county__in=counties)
        
    # Group by seat and candidate
    grouped_votes = votes_query.values(
        'seat__name', 'seat__seat_type', 'seat__level',
        'candidate__full_name', 'candidate__party'
    ).annotate(votes=Count('id')).order_by('seat__seat_type', '-votes')
    
    # Format the response
    results = {}
    for v in grouped_votes:
        stype = v['seat__seat_type']
        if stype not in results:
            results[stype] = []
        results[stype].append({
            'seat_name': v['seat__name'],
            'candidate': v['candidate__full_name'],
            'party': v['candidate__party'],
            'votes': v['votes'],
            'seat_level': v['seat__level']
        })
        
    return Response(results, status=200)

@api_view(["POST"])
def chat_response(request):
    """
    Intelligent chatbot backend using a keyword-matching engine.
    """
    user_message = request.data.get('message', '').lower()
    
    if not user_message:
        return Response({'reply': "I'm sorry, I didn't catch that. Could you please type your question?"}, status=400)
    # Define Intents and Keywords
    # Define Intents and Keywords in both languages
    intents = {
        'registration': {
            'keywords_en': ['register', 'sign up', 'create account', 'join', 'how to register', 'account'],
            'keywords_sw': ['jisajili', 'jiunge', 'akaunti', 'jinsi ya kujisajili', 'kujiandikisha'],
            'response_en': 'To register, click the "Register" button on the home page. You will need a valid Kenyan ID, your phone number, and you must select your County, Constituency, and Ward.',
            'response_sw': 'Ili kujisajili, bofya kitufe cha "Register" kwenye ukurasa wa nyumbani. Utahitaji Kitambulisho cha Taifa, nambari ya simu, na utahitajika kuchagua Kaunti, Eneo Bunge, na Wodi yako.'
        },
        'voting': {
            'keywords_en': ['vote', 'cast', 'ballot', 'how to vote', 'voting', 'elect', 'candidates'],
            'keywords_sw': ['piga kura', 'kura', 'jinsi ya kupiga kura', 'wagombea', 'chagua'],
            'response_en': 'Once logged in, navigate to the "Voting" page. You will see ballots tailored to your registered region. Simply select your preferred candidates and submit your vote. Remember, you can only vote once per seat!',
            'response_sw': 'Baada ya kuingia, nenda kwenye ukurasa wa "Kura". Utaona karatasi za kura kulingana na eneo lako. Chagua wagombea wako na uwasilishe kura yako. Kumbuka, unaweza kupiga kura mara moja tu kwa kila kiti!'
        },
        'results': {
            'keywords_en': ['results', 'leaders', 'winning', 'who is winning', 'standings', 'score', 'outcome', 'tally'],
            'keywords_sw': ['matokeo', 'viongozi', 'nani anashinda', 'mshindi'],
            'response_en': 'You can view live election results by navigating to the "Results" page from the dashboard. It shows the leading candidates nationwide in real-time.',
            'response_sw': 'Unaweza kuona matokeo moja kwa moja kwenye ukurasa wa "Matokeo". Inaonyesha wagombea wanaoongoza nchi nzima kwa wakati halisi.'
        },
        'analytics': {
            'keywords_en': ['analytics', 'filter', 'region', 'county results', 'ward results', 'province', 'breakdown', 'where is analytics', 'charts', 'graphs'],
            'keywords_sw': ['uchambuzi', 'changanua', 'mkoa', 'matokeo ya kaunti', 'chati', 'grafu', 'uchanganuzi'],
            'response_en': 'For an in-depth breakdown, click the "Analytics" button in the top navigation bar. You can filter by Province, County, and Constituency to see exactly how specific regions are voting for every candidate!',
            'response_sw': 'Kwa uchambuzi wa kina, bofya kitufe cha "Analytics" juu. Unaweza kuchuja kwa Mkoa, Kaunti, na Eneo Bunge ili kuona jinsi maeneo tofauti yanavyopiga kura!'
        },
        'password': {
            'keywords_en': ['password', 'forgot', 'reset', 'lost password', 'cant login', "can't login", 'credentials', 'change password'],
            'keywords_sw': ['nywila', 'nenosiri', 'umesahau', 'sahaulika', 'siwezi kuingia', 'badilisha nenosiri'],
            'response_en': 'If you forgot your password, please contact a system administrator to have it reset. (Currently, there is no automated password reset link for security reasons).',
            'response_sw': 'Ikiwa umesahau nenosiri lako, tafadhali wasiliana na msimamizi wa mfumo ili alibadilishe. (Kwa sasa hakuna kiungo cha kiotomatiki kwa sababu za kiusalama).'
        },
        'eligibility': {
            'keywords_en': ['who can vote', 'eligible', 'age', 'requirements', 'allowed', 'id', 'citizenship'],
            'keywords_sw': ['nani anaruhusiwa', 'vigezo', 'umri', 'kuruhusiwa', 'kitambulisho', 'uraia', 'miaka'],
            'response_en': 'Any Kenyan citizen over the age of 18 with a valid National ID or Passport who has registered on our platform can vote.',
            'response_sw': 'Raia yeyote wa Kenya aliye na umri wa miaka 18 au zaidi na Kitambulisho cha Taifa au Pasipoti halali, na aliyejisajili kwenye mfumo wetu anaweza kupiga kura.'
        },
        'admin': {
            'keywords_en': ['admin', 'dashboard', 'command center', 'halt', 'restart'],
            'keywords_sw': ['msimamizi', 'msimamizi wa mfumo', 'simamisha', 'anza tena', 'dhibiti'],
            'response_en': 'The Admin Command Center is restricted. Only authorized officials with a Root Access Key can enter. From there, they can monitor live database velocity, add candidates, or halt the election.',
            'response_sw': 'Kituo cha Usimamizi kimezuiwa. Ni maafisa walioidhinishwa tu ndio wanaoweza kuingia. Kutoka hapo, wanaweza kufuatilia mfumo, kuongeza wagombea, au kusimamisha uchaguzi.'
        },
        'greeting': {
            'keywords_en': ['hello', 'hi', 'hey', 'greetings', 'morning', 'afternoon'],
            'keywords_sw': ['jambo', 'habari', 'sasa', 'mambo', 'niaje', 'sema', 'vipi'],
            'response_en': 'Hello there! I am your Uchaguzi intelligent assistant. How can I help you with the voting platform today?',
            'response_sw': 'Jambo! Mimi ni msaidizi wako wa Uchaguzi. Naweza kukusaidiaje kuhusu mfumo wa kupiga kura leo?'
        },
        'thanks': {
            'keywords_en': ['thanks', 'thank you', 'appreciate', 'good bot'],
            'keywords_sw': ['asante', 'shukran', 'nashukuru'],
            'response_en': 'You are very welcome! If you need anything else, just ask.',
            'response_sw': 'Karibu sana! Kama unahitaji kingine, niulize tu.'
        },
        'theme': {
            'keywords_en': ['light mode', 'dark mode', 'theme', 'color', 'background', 'bright', 'dark'],
            'keywords_sw': ['rangi', 'muonekano', 'giza', 'mwangaza'],
            'response_en': 'You can switch between Light and Dark mode by clicking the circular Theme Toggle switch floating in the bottom-left corner of your screen.',
            'response_sw': 'Unaweza kubadilisha kati ya muonekano wa Mwangaza (Light) na Giza (Dark) kwa kubofya kitufe cha duara kilicho chini upande wa kushoto wa skrini yako.'
        }
    }

    best_intent = None
    max_score = 0
    language_matched = 'en'

    # Check for highest scoring keyword match across both languages
    for intent_name, intent_data in intents.items():
        for keyword in intent_data['keywords_en']:
            if keyword in user_message:
                if len(keyword) > max_score:
                    max_score = len(keyword)
                    best_intent = intent_name
                    language_matched = 'en'
        
        for keyword in intent_data['keywords_sw']:
            if keyword in user_message:
                if len(keyword) > max_score:
                    max_score = len(keyword)
                    best_intent = intent_name
                    language_matched = 'sw'

    if best_intent and max_score > 0:
        reply = intents[best_intent][f'response_{language_matched}']
    else:
        # Fallback - bilingual
        reply = "I'm sorry, I'm only trained to help with the Uchaguzi platform (registration, voting, results). Could you rephrase your question? / Samahani, nimefunzwa kusaidia na mfumo wa Uchaguzi tu (usajili, kupiga kura, matokeo). Unaweza kuuliza kwa njia nyingine?"

    return Response({'reply': reply}, status=200)