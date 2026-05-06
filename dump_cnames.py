import sys
sys.path.append(r'c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-backend')
from voting_api.mappings import WARD_LOOKUP

c_names = set(w[1] for w in WARD_LOOKUP.values())
with open(r'c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-backend\scratch_cnames.txt', 'w') as f:
    f.write("\n".join(sorted(c_names)))
