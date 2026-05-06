import re
import os

ts_path = r'c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-Frontend\src\app\shared\constituencies.ts'
py_path = r'c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-backend\voting_api\mappings.py'

with open(ts_path, 'r', encoding='utf-8') as f:
    ts_data = f.read()

constituencies = []
for match in re.finditer(r"\{\s*id:\s*(\d+),\s*name:\s*'([^']+)'", ts_data):
    constituencies.append(f'    {match.group(1)}: "{match.group(2)}",')

with open(py_path, 'r', encoding='utf-8') as f:
    py_data = f.read()

# Replace CONSTITUENCY_LOOKUP = { ... }
new_lookup = "CONSTITUENCY_LOOKUP = {\n" + "\n".join(constituencies) + "\n}"
py_data = re.sub(r'CONSTITUENCY_LOOKUP\s*=\s*\{.*\}', new_lookup, py_data, flags=re.DOTALL)

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(py_data)

print("Successfully updated CONSTITUENCY_LOOKUP in mappings.py")
