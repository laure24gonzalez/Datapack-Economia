import zipfile
import json
from pathlib import Path

JAR = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"
ROOT = Path(__file__).resolve().parents[1]
ZOMBIE_PATH = ROOT / 'data' / 'minecraft' / 'loot_table' / 'entities' / 'zombie.json'

with zipfile.ZipFile(JAR) as z:
    candidates = [n for n in z.namelist() if n.endswith('loot_table/entities/zombie.json')]
    print('jar zombie candidates:', candidates)
    if candidates:
        data = z.read(candidates[0]).decode('utf-8')
        obj = json.loads(data)
        print('jar pools:', len(obj.get('pools', [])))
        for i, pool in enumerate(obj.get('pools', [])):
            print('jar pool', i, 'keys', list(pool.keys()))
            print('jar pool', i, 'conditions', pool.get('conditions'))
            print('jar pool', i, 'entries count', len(pool.get('entries', [])))
            if i == 0:
                entry = pool.get('entries', [])[0]
                print('jar first entry type/name', entry.get('type'), entry.get('name'))
    else:
        print('no jar zombie loot table found')

print('datapack zombie exists:', ZOMBIE_PATH.exists())
if ZOMBIE_PATH.exists():
    obj = json.loads(ZOMBIE_PATH.read_text(encoding='utf-8'))
    print('dp pools:', len(obj.get('pools', [])))
    for i, pool in enumerate(obj.get('pools', [])):
        print('dp pool', i, 'keys', list(pool.keys()))
        print('dp pool', i, 'conditions', pool.get('conditions'))
        print('dp pool', i, 'entries count', len(pool.get('entries', [])))
        for entry in pool.get('entries', []):
            if entry.get('type') == 'minecraft:item' and entry.get('name') == 'minecraft:copper_nugget':
                print('  coin entry found in pool', i)
                print('  functions:', entry.get('functions'))
                print('  components present:', [f.get('function') for f in entry.get('functions', [])])
                if any(f.get('function') == 'minecraft:set_components' for f in entry.get('functions', [])):
                    comps = next(f for f in entry.get('functions', []) if f.get('function') == 'minecraft:set_components').get('components')
                    print('  set_components keys:', list(comps.keys()))
                    print('  custom_data:', comps.get('minecraft:custom_data'))
                    print('  custom_model_data:', comps.get('minecraft:custom_model_data'))
                    print('  rarity:', comps.get('minecraft:rarity'))
            elif entry.get('type') == 'minecraft:item':
                print('  non-coin item entry type/name', entry.get('type'), entry.get('name'))
