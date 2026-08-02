import json
import zipfile
from pathlib import Path

JAR = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

REPORT = {
    'load_tag': None,
    'tick_tag': None,
    'missing_functions': [],
    'pack_mcmeta': None,
    'namespaces_paths': {
        'has_loot_table_dir': False,
        'has_loot_tables_dir': False,
        'has_function_dir': False,
        'has_functions_dir': False
    },
    'json_errors': [],
    'random_sequence': {
        'jar': None,
        'datapack': None,
        'match': None
    }
}


def read_jar(path_in_jar):
    try:
        with zipfile.ZipFile(JAR) as z:
            return z.read(path_in_jar).decode('utf-8')
    except Exception as e:
        return None


def load_json(path):
    try:
        text = path.read_text(encoding='utf-8')
        return json.loads(text), None
    except Exception as e:
        return None, str(e)


def check_tag_file(tag_path):
    obj, err = load_json(tag_path)
    if err:
        return {'error': err}
    vals = obj.get('values') or obj.get('values', [])
    missing = []
    for v in vals:
        if ':' in v:
            ns, rest = v.split(':', 1)
        else:
            ns, rest = 'minecraft', v
        # convert function path to file path
        func_path = DATA / ns / 'functions' / (rest + '.mcfunction')
        if not func_path.exists():
            missing.append(str(func_path))
    return {'values': vals, 'missing': missing}


def scan_namespaces():
    base = DATA
    REPORT['namespaces_paths']['has_loot_table_dir'] = (base / 'minecraft' / 'loot_table').exists() or any((p.name == 'loot_table' for p in base.rglob('*') if p.is_dir()))
    REPORT['namespaces_paths']['has_loot_tables_dir'] = (base / 'economiarpg' / 'loot_tables').exists() or any((p.name == 'loot_tables' for p in base.rglob('*') if p.is_dir()))
    REPORT['namespaces_paths']['has_function_dir'] = (base / 'minecraft' / 'tags' / 'function').exists() or any((p.name == 'function' for p in base.rglob('*') if p.is_dir()))
    REPORT['namespaces_paths']['has_functions_dir'] = (base / 'economiarpg' / 'functions').exists() or any((p.name == 'functions' for p in base.rglob('*') if p.is_dir()))


def find_json_errors():
    for p in DATA.rglob('*.json'):
        try:
            text = p.read_text(encoding='utf-8')
            json.loads(text)
        except Exception as e:
            REPORT['json_errors'].append({'file': str(p.relative_to(ROOT)), 'error': str(e)})


def check_random_sequence(mob='zombie.json'):
    jar_path = f'data/minecraft/loot_table/entities/{mob}'
    jar_text = read_jar(jar_path)
    dp_file = DATA / 'minecraft' / 'loot_table' / 'entities' / mob
    dp_text = None
    if dp_file.exists():
        dp_text = dp_file.read_text(encoding='utf-8')
    try:
        jar_obj = json.loads(jar_text) if jar_text else None
        dp_obj = json.loads(dp_text) if dp_text else None
        REPORT['random_sequence']['jar'] = jar_obj.get('random_sequence') if jar_obj else None
        REPORT['random_sequence']['datapack'] = dp_obj.get('random_sequence') if dp_obj else None
        REPORT['random_sequence']['match'] = REPORT['random_sequence']['jar'] == REPORT['random_sequence']['datapack']
    except Exception:
        REPORT['random_sequence']['jar'] = None
        REPORT['random_sequence']['datapack'] = None
        REPORT['random_sequence']['match'] = False


def check_pack_mcmeta():
    p = ROOT / 'pack.mcmeta'
    if not p.exists():
        REPORT['pack_mcmeta'] = {'exists': False}
        return
    try:
        obj = json.loads(p.read_text(encoding='utf-8'))
        REPORT['pack_mcmeta'] = {'exists': True, 'content': obj}
    except Exception as e:
        REPORT['pack_mcmeta'] = {'exists': True, 'error': str(e)}


if __name__ == '__main__':
    # check tags/functions load and tick
    load_tag = DATA / 'minecraft' / 'tags' / 'function' / 'load.json'
    tick_tag = DATA / 'minecraft' / 'tags' / 'function' / 'tick.json'
    if load_tag.exists():
        REPORT['load_tag'] = check_tag_file(load_tag)
    else:
        REPORT['load_tag'] = {'exists': False}
    if tick_tag.exists():
        REPORT['tick_tag'] = check_tag_file(tick_tag)
    else:
        REPORT['tick_tag'] = {'exists': False}

    # scan namespaces/dirs
    scan_namespaces()

    # find json parse errors
    find_json_errors()

    # check random_sequence for zombie
    check_random_sequence('zombie.json')

    # pack.mcmeta
    check_pack_mcmeta()

    print(json.dumps(REPORT, indent=2, ensure_ascii=False))
