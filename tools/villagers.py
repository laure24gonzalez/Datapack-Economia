import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "economiarpg" / "function" / "custom_villagers"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COIN_DEFINITIONS = {
    "bronze_coin": {
        "id": "minecraft:copper_nugget",
        "name": "Moneda de bronce",
        "currency": "bronze",
        "value": 1,
        "rarity": "common",
        "lore": "Valor: 1"
    },
    "silver_coin": {
        "id": "minecraft:iron_nugget",
        "name": "Moneda de plata",
        "currency": "silver",
        "value": 10,
        "rarity": "rare",
        "lore": "Valor: 10"
    },
    "gold_coin": {
        "id": "minecraft:gold_nugget",
        "name": "Moneda de oro",
        "currency": "gold",
        "value": 100,
        "rarity": "epic",
        "lore": "Valor: 100"
    },
    "emerald_coin": {
        "id": "minecraft:emerald",
        "name": "Moneda de esmeralda",
        "currency": "emerald",
        "value": 1000,
        "rarity": "epic",
        "lore": "Valor: 1000"
    },
    "diamond_coin": {
        "id": "minecraft:diamond",
        "name": "Moneda de diamante",
        "currency": "diamond",
        "value": 10000,
        "rarity": "epic",
        "lore": "Valor: 10000"
    },
    "netherite_coin": {
        "id": "minecraft:netherite_ingot",
        "name": "Moneda de netherita",
        "currency": "netherite",
        "value": 100000,
        "rarity": "legendary",
        "lore": "Valor: 100000"
    },
    "ruby_coin": {
        "id": "minecraft:emerald",
        "name": "Moneda de rubí",
        "currency": "ruby",
        "value": 1000000,
        "rarity": "legendary",
        "lore": "Valor: 1000000"
    },
}

SELL_DEFINITIONS = {
    "legendary_chestplate": {
        "id": "minecraft:netherite_chestplate",
        "components": {
            "minecraft:enchantments": {
                "levels": {
                    "minecraft:protection": 10,
                    "minecraft:projectile_protection": 10,
                    "minecraft:blast_protection": 10,
                    "minecraft:fire_protection": 10,
                    "minecraft:thorns": 5,
                    "minecraft:unbreaking": 10,
                    "minecraft:mending": 8,
                }
            },
            "minecraft:attribute_modifiers": {
                "modifiers": [
                    {
                        "id": "economiarpg:chestplate_health",
                        "type": "minecraft:max_health",
                        "amount": 8,
                        "operation": "add_value",
                        "slot": "chest"
                    }
                ]
            }
        }
    },
    "legendary_sword": {
        "id": "minecraft:netherite_sword",
        "components": {
            "minecraft:enchantments": {
                "levels": {
                    "minecraft:sharpness": 10,
                    "minecraft:smite": 8,
                    "minecraft:banes_of_arthropods": 5,
                    "minecraft:looting": 5,
                    "minecraft:fire_aspect": 1,
                    "minecraft:unbreaking": 10,
                    "minecraft:mending": 2,
                }
            }
        }
    },
    "legendary_pickaxe": {
        "id": "minecraft:netherite_pickaxe",
        "components": {
            "minecraft:enchantments": {
                "levels": {
                    "minecraft:efficiency": 10,
                    "minecraft:fortune": 5,
                    "minecraft:unbreaking": 10,
                    "minecraft:mending": 8,
                }
            }
        }
    },
    "totem_of_undying": {
        "id": "minecraft:totem_of_undying",
        "components": {}
    },
    "end_crystal": {
        "id": "minecraft:end_crystal",
        "components": {}
    },
}

SHOPS = [
    {"shop": "blacksmith", "name": "Herrero Legendario", "profession": "minecraft:armorer", "buy": "netherite_coin", "price": 12, "sell": "legendary_chestplate"},
    {"shop": "armorer", "name": "Armero Legendario", "profession": "minecraft:armorer", "buy": "netherite_coin", "price": 15, "sell": "legendary_sword"},
    {"shop": "tools", "name": "Herramientas Legendarias", "profession": "minecraft:toolsmith", "buy": "netherite_coin", "price": 15, "sell": "legendary_pickaxe"},
    {"shop": "utilities", "name": "Utilidades Especiales", "profession": "minecraft:cleric", "buy": "diamond_coin", "price": 3, "sell": "totem_of_undying"},
]


def build_coin_component(coin_key: str) -> dict:
    coin = COIN_DEFINITIONS[coin_key]
    return {
        "id": coin["id"],
        "count": 1,
        "components": {
            "minecraft:item_name": {"text": coin["name"], "color": "gold", "bold": True},
            "minecraft:lore": [{"text": coin["lore"], "color": "gray", "bold": True, "italic": False}],
            "minecraft:rarity": coin["rarity"],
            "minecraft:custom_data": {
                "economiarpg": {
                    "type": "coin",
                    "currency": coin["currency"],
                    "value": coin["value"],
                }
            },
        }
    }


def build_sell_component(item_key: str) -> dict:
    item = SELL_DEFINITIONS[item_key]
    return {
        "id": item["id"],
        "count": 1,
        "components": item["components"],
    }


def build_recipe(entry: dict) -> dict:
    return {
        "rewardExp": 0,
        "maxUses": 2147483647,
        "buy": {
            **build_coin_component(entry["buy"]),
            "count": entry["price"],
        },
        "sell": build_sell_component(entry["sell"]),
    }


def build_summon_command(entry: dict) -> str:
    return (
        "summon minecraft:villager ~ ~ ~ {"
        "Invulnerable:1b,NoAI:1b,Silent:1b,PersistenceRequired:1b,"
        f"CustomName:'{{\"text\":\"{entry['name']}\",\"color\":\"gold\",\"bold\":true}}',"
        "CustomNameVisible:1b,"
        f"VillagerData:{{profession:\"{entry['profession']}\",level:5,type:\"minecraft:plains\"}},"
        "Offers:{Recipes:[]}"
        "}"
    )


for entry in SHOPS:
    path = OUTPUT_DIR / f"{entry['shop']}_shop.mcfunction"
    path.write_text(build_summon_command(entry) + "\n", encoding="utf-8")
    print(f"Wrote {path}")

master_path = OUTPUT_DIR / "spawn_all_shopkeepers.mcfunction"
master_lines = ["# Generated shopkeeper spawns"]
for entry in SHOPS:
    master_lines.append(f"function economiarpg:custom_villagers/{entry['shop']}_shop")
master_path.write_text("\n".join(master_lines) + "\n", encoding="utf-8")
print(f"Wrote {master_path}")
