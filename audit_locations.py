import re

path = r'c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-Frontend\src\app\components\registration\registration.ts'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Separate into constituencies array and wards array based on text location
c_match = re.search(r'const CONSTITUENCIES =.*?\[(.*?)\];', text, re.DOTALL)
w_match = re.search(r'const WARDS =.*?\[(.*?)\];', text, re.DOTALL)

constituencies = {}
if c_match:
    for line in c_match.group(1).split('\n'):
        matches = re.finditer(r'id:\s*(\d+),\s*name:\s*[\'"]([^\'"]+)[\'"]', line)
        for m in matches:
            constituencies[int(m.group(1))] = m.group(2).strip()

errors = []
current_expected_constituency = ""

if w_match:
    for line_num, line in enumerate(w_match.group(1).split('\n'), start=1):
        if line.strip().startswith('//') and '-' in line:
            parts = line.split('-')
            if len(parts) >= 2:
                current_expected_constituency = parts[1].strip().lower().replace(' ', '')
                
        ward_m = re.search(r'name:\s*[\'"]([^\'"]+)[\'"].*?constituencyId:\s*(\d+)', line)
        if ward_m and current_expected_constituency:
            w_name = ward_m.group(1)
            w_cid = int(ward_m.group(2))
            actual_const_name = constituencies.get(w_cid, "").lower().replace(' ', '')
            
            # If the expected constituency name is not a substring of the actual constituency name
            # and actual is not a substring of expected (to handle "Mathioya" vs "Mathioya Central")
            if current_expected_constituency not in actual_const_name and actual_const_name not in current_expected_constituency:
                if actual_const_name:
                    errors.append(f"Collision on {w_name}: Comment says '{current_expected_constituency}', but ID {w_cid} is assigned to '{actual_const_name}'")

with open('report.txt', 'w', encoding='utf-8') as f:
    for e in errors:
        f.write(e + '\n')
