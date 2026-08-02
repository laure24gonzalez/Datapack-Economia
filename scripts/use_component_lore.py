import json
from pathlib import Path

path = Path('data/minecraft/loot_table/entities/zombie.json')
data = json.loads(path.read_text(encoding='utf-8'))
for pool in data.get('pools', []):
    for entry in pool.get('entries', []):
        if entry.get('name') == 'minecraft:copper_nugget':
            entry['functions'] = [
                {
                    'function': 'minecraft:set_count',
                    'count': 1,
                },
                {
                    'function': 'minecraft:set_components',
                    'components': {
                        'minecraft:custom_name': {
                            'text': 'Moneda de bronce',
                            'color': 'red',
                            'bold': True,
                        },
                        'minecraft:lore': [
                            {
                                'text': 'Valor: 1',
                                'color': 'gray',
                                'italic': False,
                                'bold': True,
                            }
                        ],
                        'minecraft:custom_data': {
                            'economiarpg': {
                                'type': 'coin',
                                'id': 'bronze_coin',
                                'currency': 'bronze',
                                'value': 1,
                            }
                        },
                        'minecraft:custom_model_data': 1,
                    }
                },
            ]
            break
    else:
        continue
    break

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(path)
