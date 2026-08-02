import zipfile
import json
import difflib
from pathlib import Path

JAR = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"
ROOT = Path(__file__).resolve().parents[1]
LOOT_PATH = ROOT / 'data' / 'minecraft' / 'loot_table' / 'entities'

def read_jar(path_in_jar):
    with zipfile.ZipFile(JAR) as z:
        return z.read(path_in_jar).decode('utf-8')

def read_datapack(path):
    return path.read_text(encoding='utf-8')

def analyze_json(jar_json_text, dp_json_text):
    jar_obj = json.loads(jar_json_text)
    dp_obj = json.loads(dp_json_text)

    def has_coin_pool(obj):
        for pool in obj.get('pools', []):
            for entry in pool.get('entries', []):
                if entry.get('type') == 'minecraft:item' and entry.get('name', '') == 'minecraft:copper_nugget':
                    for func in entry.get('functions', []):
                        if func.get('function') == 'minecraft:set_components':
                            comps = func.get('components', {})
                            if 'minecraft:custom_data' in comps and comps['minecraft:custom_data'].get('economiarpg', {}).get('type') == 'coin':
                                return True
        return False

    return {
        'jar_has_coin_pool': has_coin_pool(jar_obj),
        'dp_has_coin_pool': has_coin_pool(dp_obj),
        'jar_pools': len(jar_obj.get('pools', [])),
        'dp_pools': len(dp_obj.get('pools', [])),
    }


def unified_diff(a, b, fromfile, tofile):
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    return '\n'.join(difflib.unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile, n=3))

def compare(mob_name='zombie.json'):
    jar_path = f'data/minecraft/loot_table/entities/{mob_name}'
    dp_path = LOOT_PATH / mob_name
    if not dp_path.exists():
        print(f'Datapack loot file missing: {dp_path}')
        return 2
    try:
        jar_text = read_jar(jar_path)
    except KeyError:
        print(f'Vanilla jar missing {jar_path}')
        return 2
    dp_text = read_datapack(dp_path)
    diff = unified_diff(jar_text, dp_text, f'jar:{mob_name}', f'datapack:{mob_name}')
    print('--- UNIFIED DIFF ---')
    print(diff)
    print('\n--- ANALYSIS ---')
    analysis = analyze_json(jar_text, dp_text)
    for k,v in analysis.items():
        print(f'{k}: {v}')
    return 0

if __name__ == '__main__':
    import sys
    mob = 'zombie.json'
    if len(sys.argv) > 1:
        mob = sys.argv[1]
    sys.exit(compare(mob))
