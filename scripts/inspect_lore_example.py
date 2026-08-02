import json
import zipfile

jar = r'c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar'
with zipfile.ZipFile(jar) as z:
    for name in ['data/minecraft/loot_table/chests/shipwreck_map.json', 'data/minecraft/loot_table/chests/underwater_ruin_big.json', 'data/minecraft/loot_table/equipment/trial_chamber.json']:
        data = json.loads(z.read(name).decode('utf-8'))
        print('---', name)
        for pool in data.get('pools', []):
            for entry in pool.get('entries', []):
                for fn in entry.get('functions', []):
                    if fn.get('function') in {'minecraft:set_name', 'minecraft:set_lore', 'minecraft:set_components'}:
                        print(json.dumps(fn, indent=2))
                        raise SystemExit
