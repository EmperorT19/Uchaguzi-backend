import re
import os

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
        for m in re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*(['\"])(.*?)(?<!\\)\2", county_match.group(1)):
            counties[int(m.group(1))] = m.group(3)

    # Parse constituencies from constituencies.ts
    constituencies = {}
    for m in re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*(['\"])(.*?)(?<!\\)\2,\s*countyId:\s*(\d+)\s*\}", const_data):
        constituencies[int(m.group(1))] = {
            'name': m.group(3),
            'countyId': int(m.group(4))
        }

    # Parse wards from registration.ts
    wards = {}
    ward_match = re.search(r'wards\s*=\s*signal<any>\(\[\s*(.*?)\]\);', reg_data, re.DOTALL)
    if not ward_match:
        ward_match = re.search(r'wards\s*=\s*signal<any>\(\[\s*(.*?)\s*\]\);', reg_data, re.DOTALL)
    
    if ward_match:
        for m in re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*(['\"])(.*?)(?<!\\)\2,\s*constituencyId:\s*(\d+)\s*\}", ward_match.group(1)):
            wards[int(m.group(1))] = {
                'name': m.group(3),
                'constituencyId': int(m.group(4))
            }

    # Generate new WARD_LOOKUP string
    lines = []
    lines.append("WARD_LOOKUP = {")
    for w_id in sorted(wards.keys()):
        w_info = wards[w_id]
        c_id = w_info['constituencyId']
        c_info = constituencies[c_id]
        county_name = counties[c_info['countyId']]
        
        # Unescape TS quotes, then escape for Python
        w_name = w_info['name'].replace(r"\'", "'").replace(r'\"', '"').replace("'", "\\'")
        c_name = c_info['name'].replace(r"\'", "'").replace(r'\"', '"').replace("'", "\\'")
        county_name = county_name.replace(r"\'", "'").replace(r'\"', '"').replace("'", "\\'")
        
        lines.append(f"    {w_id}: ('{w_name}', '{c_name}', '{county_name}'),")
    lines.append("}")
    
    new_lookup_str = "\n".join(lines)

    # Read existing mappings.py
    with open(mappings_py, 'r', encoding='utf-8') as f:
        py_data = f.read()

    # Replace WARD_LOOKUP = { ... }
    py_data = re.sub(r'WARD_LOOKUP\s*=\s*\{.*?\}', new_lookup_str, py_data, flags=re.DOTALL)

    with open(mappings_py, 'w', encoding='utf-8') as f:
        f.write(py_data)
        
    print("SUCCESS: mappings.py has been completely regenerated with the correct WARD_LOOKUP mapping.")

if __name__ == "__main__":
    main()
