import json
import zipfile

jar = r'c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar'
with zipfile.ZipFile(jar) as z:
    data = json.loads(z.read('data/minecraft/loot_table/chests/shipwreck_map.json').decode('utf-8'))
    for pool in data.get('pools', []):
        for entry in pool.get('entries', []):
            for fn in entry.get('functions', []):
                if fn.get('function') == 'minecraft:set_name':
                    print(json.dumps(fn, indent=2))
                    raise SystemExit
