import re
with open('c:/Users/Emperor/Desktop/New stuff/Chagua/Uchaguzi-Frontend/src/app/components/registration/registration.ts', 'r', encoding='utf-8') as f:
    content = f.read()

print('CONSTITUENCY_LOOKUP = {')
for line in content.split('\n'):
    if 'countyId:' in line and '{ id:' in line:
        m = re.search(r'\{ id:\s*(\d+),\s*name:\s*\'([^\']+)\'', line)
        if m:
            print(f'    {m.group(1)}: \"{m.group(2)}\",')
print('}')
