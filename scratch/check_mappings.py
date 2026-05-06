import re
import os
import ast

def main():
    base_dir = r"c:\Users\Emperor\Desktop\New stuff\Chagua"
    reg_ts = os.path.join(base_dir, r"Uchaguzi-Frontend\src\app\components\registration\registration.ts")
    const_ts = os.path.join(base_dir, r"Uchaguzi-Frontend\src\app\shared\constituencies.ts")
    mappings_py = os.path.join(base_dir, r"Uchaguzi-backend\voting_api\mappings.py")

    with open(reg_ts, 'r', encoding='utf-8') as f:
        reg_data = f.read()

    with open(const_ts, 'r', encoding='utf-8') as f:
        const_data = f.read()

    # Parse counties from registration.ts
    counties = {}
    county_match = re.search(r'counties:\s*any\[\]\s*=\s*\[(.*?)\];', reg_data, re.DOTALL)
    if county_match:
        for m in re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*'([^']+)'", county_match.group(1)):
            counties[int(m.group(1))] = m.group(2)
    else:
        print("Counties not found")

    # Parse constituencies from constituencies.ts
    constituencies = {}
    for m in re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*'([^']+)',\s*countyId:\s*(\d+)\s*\}", const_data):
        constituencies[int(m.group(1))] = {
            'name': m.group(2),
            'countyId': int(m.group(3))
        }

    # Parse wards from registration.ts
    wards = {}
    ward_match = re.search(r'wards\s*=\s*signal<any>\(\[\s*(.*?)\]\);', reg_data, re.DOTALL)
    if not ward_match:
        ward_match = re.search(r'wards\s*=\s*signal<any>\(\[\s*(.*?)\s*\]\);', reg_data, re.DOTALL)
    
    if ward_match:
        for m in re.finditer(r'\{\s*id:\s*(\d+),\s*name:\s*"([^"]+)",\s*constituencyId:\s*(\d+)\s*\}', ward_match.group(1)):
            wards[int(m.group(1))] = {
                'name': m.group(2),
                'constituencyId': int(m.group(3))
            }
    else:
        print("Wards not found")

    # Generate new WARD_LOOKUP
    new_lookup = {}
    for w_id, w_info in wards.items():
        c_id = w_info['constituencyId']
        c_info = constituencies[c_id]
        county_name = counties[c_info['countyId']]
        new_lookup[w_id] = (w_info['name'], c_info['name'], county_name)

    # Read existing mappings.py
    import sys
    sys.path.append(os.path.join(base_dir, "Uchaguzi-backend"))
    from voting_api.mappings import WARD_LOOKUP as old_lookup

    diffs = 0
    for w_id, new_val in new_lookup.items():
        if w_id in old_lookup:
            if old_lookup[w_id] != new_val:
                print(f"Diff Ward {w_id}: {old_lookup[w_id]} -> {new_val}")
                diffs += 1
        else:
            print(f"New Ward {w_id}: {new_val}")
    
    print(f"Total diffs: {diffs}")

if __name__ == "__main__":
    main()
