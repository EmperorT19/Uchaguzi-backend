import re

path = r'c:\Users\Emperor\Desktop\New stuff\Chagua\Uchaguzi-Frontend\src\app\components\registration\registration.ts'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

keywords = ['Westlands', 'Kapseret', 'Kisumu Central', 'Mvita', 'Machakos Town', 'Parklands', 'Karura', 'Kaloleni', 'Railways', 'Tudor', 'Majengo', 'Langas', 'Megun', 'Mutituni', 'Muvuti']

print('MAP = {')
for line in text.split('\n'):
    if 'id:' in line and 'name:' in line:
        for k in keywords:
            if k in line:
                match = re.search(r'id:\s*(\d+)', line)
                if match:
                    print(f'  \"{k}\": {match.group(1)},')
print('}')
