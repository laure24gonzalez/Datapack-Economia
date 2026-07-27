import json
import zipfile
from pathlib import Path

root = Path(r"c:\Users\laure\AppData\Roaming\.minecraft\saves\Mundo nuevo\datapacks\EconomiaRPG\data\minecraft\loot_table\entities")
jar = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"

mob_specs = {
    "zombie.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 1, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "baby_zombie.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 4, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "husk.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 1, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "drowned.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "skeleton.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "bogged.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "stray.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 3, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "parched.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 3, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "creeper.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 3, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "spider.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "cave_spider.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 3, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "slime.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "silverfish.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 1, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "endermite.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 1, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "phantom.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 3, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "enderman.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 4, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "blaze.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 1, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "ghast.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "magma_cube.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "witch.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "pillager.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "vindicator.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 3, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "ravager.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 5, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "wither_skeleton.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 4, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "piglin.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "piglin_brute.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 4, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "zoglin.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 3, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "hoglin.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 3, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "guardian.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "elder_guardian.json": {"coin_name": "minecraft:gold_nugget", "coin_count": 1, "name_text": "Moneda de oro", "color": "gold", "rarity": "epic", "currency": "gold", "value": 100},
    "breeze.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "evoker.json": {"coin_name": "minecraft:gold_nugget", "coin_count": 1, "name_text": "Moneda de oro", "color": "gold", "rarity": "epic", "currency": "gold", "value": 100},
    "warden.json": {"coin_name": "minecraft:gold_nugget", "coin_count": 8, "name_text": "Moneda de oro", "color": "gold", "rarity": "epic", "currency": "gold", "value": 100},
    "wither.json": {"coin_name": "minecraft:gold_nugget", "coin_count": 10, "name_text": "Moneda de oro", "color": "gold", "rarity": "epic", "currency": "gold", "value": 100},
    "ender_dragon.json": {"coin_name": "minecraft:gold_nugget", "coin_count": 20, "name_text": "Moneda de oro", "color": "gold", "rarity": "epic", "currency": "gold", "value": 100},
    "illusioner.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 3, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "shulker.json": {"coin_name": "minecraft:iron_nugget", "coin_count": 2, "name_text": "Moneda de plata", "color": "aqua", "rarity": "rare", "currency": "silver", "value": 10},
    "vex.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 1, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "zombie_villager.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "zombified_piglin.json": {"coin_name": "minecraft:copper_nugget", "coin_count": 2, "name_text": "Moneda de bronce", "color": "red", "rarity": "common", "currency": "bronze", "value": 1},
    "giant.json": {"coin_name": "minecraft:gold_nugget", "coin_count": 5, "name_text": "Moneda de oro", "color": "gold", "rarity": "epic", "currency": "gold", "value": 100},
}

root.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(jar) as z:
    for filename, spec in mob_specs.items():
        target_path = root / filename
        if target_path.exists():
            try:
                existing = target_path.read_text(encoding="utf-8")
            except Exception:
                existing = ""
            if '"economiarpg"' in existing:
                print(f"SKIP {filename}: already has coin pool")
                continue

        internal = f"data/minecraft/loot_table/entities/{Path(filename).stem}.json"
        if internal not in z.namelist():
            internal = f"data/minecraft/loot_table/entities/{filename}"
        if internal not in z.namelist():
            print(f"SKIP {filename}: no vanilla loot table found")
            continue

        data = json.loads(z.read(internal).decode("utf-8"))
        data["pools"] = data.get("pools", []) + [{
            "rolls": 1.0,
            "bonus_rolls": 0.0,
            "conditions": [{"condition": "minecraft:killed_by_player"}],
            "entries": [{
                "type": "minecraft:item",
                "name": spec["coin_name"],
                "functions": [
                    {"function": "minecraft:set_count", "count": spec["coin_count"]},
                    {"function": "minecraft:set_name", "name": {"text": spec["name_text"], "color": spec["color"], "bold": True}},
                    {
                        "function": "minecraft:set_components",
                        "components": {
                            "minecraft:lore": [{"text": f"Valor: {spec['value']}", "color": "gray", "italic": False, "bold": True}],
                            "minecraft:custom_data": {"economiarpg": {"type": "coin", "currency": spec["currency"], "value": spec["value"]}},
                            "minecraft:rarity": spec["rarity"],
                        },
                    },
                ],
            }],
        }]

        with target_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

        print(f"Updated {filename}")
