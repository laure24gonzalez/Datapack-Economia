import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_LOOT_TABLES = ROOT / "data" / "minecraft" / "loot_table" / "entities"
JAR = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"
COIN_DIR = ROOT / "data" / "economiarpg" / "coins"
ASSETS_DIR = ROOT / "assets"

MOB_COIN_SPECS = {
    "zombie.json": {"coin_id": "bronze_coin", "coin_count": 1},
    "baby_zombie.json": {"coin_id": "bronze_coin", "coin_count": 4},
    "husk.json": {"coin_id": "bronze_coin", "coin_count": 1},
    "drowned.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "skeleton.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "bogged.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "stray.json": {"coin_id": "bronze_coin", "coin_count": 3},
    "parched.json": {"coin_id": "bronze_coin", "coin_count": 3},
    "creeper.json": {"coin_id": "bronze_coin", "coin_count": 3},
    "spider.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "cave_spider.json": {"coin_id": "bronze_coin", "coin_count": 3},
    "slime.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "silverfish.json": {"coin_id": "bronze_coin", "coin_count": 1},
    "endermite.json": {"coin_id": "bronze_coin", "coin_count": 1},
    "phantom.json": {"coin_id": "bronze_coin", "coin_count": 3},
    "enderman.json": {"coin_id": "bronze_coin", "coin_count": 4},
    "blaze.json": {"coin_id": "silver_coin", "coin_count": 1},
    "ghast.json": {"coin_id": "silver_coin", "coin_count": 2},
    "magma_cube.json": {"coin_id": "silver_coin", "coin_count": 2},
    "witch.json": {"coin_id": "silver_coin", "coin_count": 2},
    "pillager.json": {"coin_id": "silver_coin", "coin_count": 2},
    "vindicator.json": {"coin_id": "silver_coin", "coin_count": 3},
    "ravager.json": {"coin_id": "silver_coin", "coin_count": 5},
    "wither_skeleton.json": {"coin_id": "silver_coin", "coin_count": 4},
    "piglin.json": {"coin_id": "silver_coin", "coin_count": 2},
    "piglin_brute.json": {"coin_id": "silver_coin", "coin_count": 4},
    "zoglin.json": {"coin_id": "silver_coin", "coin_count": 3},
    "hoglin.json": {"coin_id": "silver_coin", "coin_count": 3},
    "guardian.json": {"coin_id": "silver_coin", "coin_count": 2},
    "elder_guardian.json": {"coin_id": "gold_coin", "coin_count": 1},
    "breeze.json": {"coin_id": "silver_coin", "coin_count": 2},
    "evoker.json": {"coin_id": "gold_coin", "coin_count": 1},
    "warden.json": {"coin_id": "gold_coin", "coin_count": 8},
    "wither.json": {"coin_id": "gold_coin", "coin_count": 10},
    "ender_dragon.json": {"coin_id": "gold_coin", "coin_count": 20},
    "illusioner.json": {"coin_id": "silver_coin", "coin_count": 3},
    "shulker.json": {"coin_id": "silver_coin", "coin_count": 2},
    "vex.json": {"coin_id": "bronze_coin", "coin_count": 1},
    "zombie_villager.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "zombified_piglin.json": {"coin_id": "bronze_coin", "coin_count": 2},
    "giant.json": {"coin_id": "gold_coin", "coin_count": 5},
}


def load_coin_definitions(coin_dir: Path) -> dict:
    coin_dir.mkdir(parents=True, exist_ok=True)
    definitions = {}
    for path in sorted(coin_dir.glob("*.json")):
        if path.name == "manifest.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        coin_id = data.get("id")
        if not coin_id:
            raise ValueError(f"Coin definition missing 'id' in {path}")
        definitions[coin_id] = data
    return definitions


def build_coin_registry(coin_definitions: dict) -> dict:
    return {
        coin_definition["id"]: {
            "id": coin_definition["id"],
            "item": coin_definition["item"],
            "display_name": coin_definition.get("display_name", coin_definition["id"]),
            "currency": coin_definition["currency"],
            "value": coin_definition["value"],
            "rarity": coin_definition.get("rarity", "common"),
            "color": coin_definition.get("color", "white"),
            "item_model": coin_definition.get("item_model"),
        }
        for coin_definition in sorted(coin_definitions.values(), key=lambda item: item["id"])
    }


def build_model_data_map(coin_definitions: dict) -> dict:
    # Allow explicit `model_data` in coin definitions. If provided, use it.
    explicit = {}
    for coin in coin_definitions.values():
        md = coin.get("model_data")
        if md is not None:
            explicit[coin["id"]] = int(md)

    used = set(explicit.values())
    result: dict = {}
    next_md = 1
    for coin in sorted(coin_definitions.values(), key=lambda item: item["id"]):
        cid = coin["id"]
        if cid in explicit:
            result[cid] = explicit[cid]
        else:
            while next_md in used:
                next_md += 1
            result[cid] = next_md
            used.add(next_md)
            next_md += 1
    return result


def build_coin_components(coin_definition: dict, custom_model_data: int | None = None) -> dict:
    lore_lines = coin_definition.get("lore") or [f"Valor: {coin_definition.get('value', 1)}"]
    display = {
        "Name": json.dumps(
            {
                "text": coin_definition.get("display_name", "Moneda"),
                "color": coin_definition.get("color", "white"),
                "bold": True,
            },
            ensure_ascii=False,
        ),
        "Lore": [
            json.dumps(
                {"text": line, "color": "gray", "italic": False, "bold": True},
                ensure_ascii=False,
            )
            for line in lore_lines
        ],
    }
    components = {
        "display": display,
        "minecraft:custom_data": {
            "economiarpg": {
                "type": "coin",
                "id": coin_definition["id"],
                "currency": coin_definition["currency"],
                "value": coin_definition["value"],
            }
        },
        "rarity": coin_definition.get("rarity", "common"),
    }
    if custom_model_data is not None:
        components["CustomModelData"] = custom_model_data
    return components


def build_coin_pool(coin_definition: dict, coin_count: int, custom_model_data: int | None = None) -> dict:
    components = build_coin_components(coin_definition, custom_model_data=custom_model_data)
    nbt_tag = build_coin_nbt_tag(components)
    return {
        "rolls": 1.0,
        "bonus_rolls": 0.0,
        "entries": [
            {
                "type": "minecraft:item",
                "name": coin_definition["item"],
                "functions": [
                    {"function": "minecraft:set_count", "count": coin_count},
                    {"function": "minecraft:set_nbt", "tag": nbt_tag},
                ],
            }
        ],
    }


def _encode_snbt_string(value: str) -> str:
    return value.replace('\\', '\\\\').replace('"', '\\\"')


def _format_json_string_for_snbt(data: dict) -> str:
    json_text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return _encode_snbt_string(json_text)


def _snbt_value(value: object) -> str:
    if isinstance(value, str):
        return '"' + value.replace('"', '\\"') + '"'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        items = [f"{k}:{_snbt_value(v)}" for k, v in value.items()]
        return "{" + ",".join(items) + "}"
    if isinstance(value, list):
        return "[" + ",".join(_snbt_value(v) for v in value) + "]"
    raise TypeError(f"Unsupported SNBT value type: {type(value)}")


def build_coin_nbt_tag(components: dict) -> str:
    tag_parts: list[str] = []
    for key, value in components.items():
        tag_parts.append(f"{key}:{_snbt_value(value)}")
    return "{" + ",".join(tag_parts) + "}"


def build_coin_item_tag(coin_definition: dict, custom_model_data: int | None = None) -> str:
    components = build_coin_components(coin_definition, custom_model_data=custom_model_data)
    return build_coin_nbt_tag(components)


def build_give_command(coin_definition: dict, count: int = 1, player: str = "@p", custom_model_data: int | None = None) -> str:
    item_tag = build_coin_item_tag(coin_definition, custom_model_data=custom_model_data)
    return f"give {player} {coin_definition['item']}{item_tag} {count}"


def write_give_commands(coin_definitions: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Generated coin commands"]
    model_data_map = build_model_data_map(coin_definitions)
    for coin_definition in sorted(coin_definitions.values(), key=lambda item: item["id"]):
        lines.append(build_give_command(coin_definition, custom_model_data=model_data_map[coin_definition["id"]]))
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_coin_manifest(coin_definitions: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_coin_registry(coin_definitions)
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_help_function(coin_definitions: dict, output_path: Path) -> None:
    """Write a simple help mcfunction that prints available commands and usage."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append('tellraw @a {"text":"EconomiaRPG - Comandos disponibles:","color":"gold"}')
    lines.append('tellraw @a {"text":"Ejecuta /function economiarpg:generated_coin_commands para obtener ejemplos de /give preparados.","color":"yellow"}')
    lines.append('tellraw @a {"text":"También puedes usar /give con el item y custom_model_data correspondiente (ver data/economiarpg/coins).","color":"gray"}')
    lines.append('tellraw @a {"text":"Ejecuta /function economiarpg:compare_coin_items para comparar el item de loot con el item de /give.","color":"aqua"}')

    # Add per-coin hints
    model_data_map = build_model_data_map(coin_definitions)
    for coin in sorted(coin_definitions.values(), key=lambda c: c["id"]):
        item = coin["item"]
        item_tag = build_coin_item_tag(coin, custom_model_data=model_data_map[coin["id"]])
        cmd_example = f"/give @p {item}{item_tag} 1"
        escaped = cmd_example.replace('"', '\\"')
        lines.append(f'tellraw @a {{"text":"{escaped}","color":"green"}}')

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_coin_test_loot_table(coin_definitions: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    bronze_coin = coin_definitions.get("bronze_coin")
    if bronze_coin is None:
        raise KeyError("Missing coin definition for bronze_coin")
    model_data_map = build_model_data_map(coin_definitions)
    loot_table = {
        "pools": [
            build_coin_pool(bronze_coin, coin_count=1, custom_model_data=model_data_map[bronze_coin["id"]])
        ]
    }
    output_path.write_text(json.dumps(loot_table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_coin_comparison_function(coin_definitions: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    coin_definition = coin_definitions.get("bronze_coin")
    if coin_definition is None:
        raise KeyError("Missing coin definition for bronze_coin")
    model_data_map = build_model_data_map(coin_definitions)
    item_tag = build_coin_item_tag(coin_definition, custom_model_data=model_data_map[coin_definition["id"]])

    lines: list[str] = []
    lines.append('# Compare la moneda generada por loot con la moneda generada por /give')
    lines.append('clear @p')
    lines.append('loot give @p loot economiarpg:test_bronze_coin')
    lines.append(f'give @p {coin_definition["item"]}{item_tag} 1')
    lines.append('tellraw @a {"text":"Selecciona cada item y ejecuta /data get entity @p SelectedItem para comparar el NBT.","color":"yellow"}')
    lines.append('tellraw @a {"text":"La primera moneda es la de loot table y la segunda es la moneda creada con /give.","color":"gold"}')

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_villager_trader_function(coin_definitions: dict, output_path: Path) -> None:
    """Generate a mcfunction that summons a villager with trades accepting the defined coins.

    Each offer will buy 1 `minecraft:copper_nugget` with matching `economiarpg` tag and
    `CustomModelData` and sell a small payment (example: emerald). This is an example
    trader for testing and can be adapted later.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    model_data_map = build_model_data_map(coin_definitions)
    offers = []
    for coin in sorted(coin_definitions.values(), key=lambda c: model_data_map[c["id"]]):
        md = model_data_map[coin["id"]]
        item_tag = build_coin_item_tag(coin, custom_model_data=md)
        buy_snbt = '{id:"' + coin["item"] + '",Count:1b,tag:' + item_tag + '}'
        sell_snbt = '{id:"minecraft:emerald",Count:1b}'
        offer = (
            '{buy:' + buy_snbt + ',sell:' + sell_snbt + ',maxUses:999999,experience:0,priceMultiplier:0.0}'
        )
        offers.append(offer)

    offers_list = ",".join(offers)
    summon_cmd = (
        'summon villager ~ ~1 ~ {VillagerData:{profession:farmer,level:2,type:plains},Offers:{Recipes:['
        + offers_list + ']}}'
    )

    # Write to file as a single command
    output_path.write_text(summon_cmd + "\n", encoding="utf-8")


def write_resource_pack_assets(coin_definitions: dict) -> None:
    model_dir = ASSETS_DIR / "economiarpg" / "models" / "item"
    model_dir.mkdir(parents=True, exist_ok=True)

    coin_definitions_sorted = sorted(coin_definitions.values(), key=lambda item: item["id"])
    for coin_definition in coin_definitions_sorted:
        model_path = model_dir / f"{coin_definition['id']}.json"
        model_path.write_text(json.dumps({
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"economiarpg:item/{coin_definition['id']}"}
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    grouped_by_item = {}
    for coin_definition in coin_definitions_sorted:
        base_item = coin_definition["item"].split(":", 1)[1] if ":" in coin_definition["item"] else coin_definition["item"]
        grouped_by_item.setdefault(base_item, []).append(coin_definition)

    model_data_map = build_model_data_map(coin_definitions)
    for base_item, matching_coins in grouped_by_item.items():
        base_model_path = ASSETS_DIR / "minecraft" / "models" / "item" / f"{base_item}.json"
        base_model_path.parent.mkdir(parents=True, exist_ok=True)
        overrides = []
        for coin_definition in sorted(matching_coins, key=lambda item: model_data_map[item["id"]]):
            overrides.append({
                "predicate": {"custom_model_data": model_data_map[coin_definition["id"]]},
                "model": f"economiarpg:item/{coin_definition['id']}"
            })
        # Always use the vanilla texture as the base layer so the unmodified item
        # (without CustomModelData) keeps its vanilla appearance. Use overrides
        # to map specific CustomModelData values to the economiarpg coin models.
        base_layer = f"minecraft:item/{base_item}"

        base_model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": base_layer},
        }
        if overrides:
            base_model["overrides"] = overrides
        base_model_path.write_text(json.dumps(base_model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_resource_pack_zip(assets_dir: Path, output_zip: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "pack": {
            "pack_format": 75.0,
            "description": "EconomiaRPG",
        }
    }

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(assets_dir.rglob("*")):
            if path.is_file():
                rel_path = path.relative_to(assets_dir)
                zf.write(path, arcname=f"assets/{rel_path.as_posix()}")
        zf.writestr("pack.mcmeta", json.dumps(manifest, ensure_ascii=False) + "\n")


def is_coin_pool(pool: dict) -> bool:
    for entry in pool.get("entries", []):
        for function in entry.get("functions", []):
            if function.get("function") == "minecraft:set_custom_data":
                tag = function.get("tag", {})
                if tag.get("economiarpg", {}).get("type") == "coin":
                    return True
            if function.get("function") == "minecraft:set_components":
                components = function.get("components", {})
                custom_data = components.get("minecraft:custom_data", {})
                if custom_data.get("economiarpg", {}).get("type") == "coin":
                    return True
    return False


def upsert_coin_pool(data: dict, coin_pool: dict) -> None:
    pools = data.get("pools", [])
    replaced = False
    updated_pools = []
    for pool in pools:
        if not replaced and is_coin_pool(pool):
            updated_pools.append(coin_pool)
            replaced = True
        else:
            updated_pools.append(pool)
    if not replaced:
        updated_pools.append(coin_pool)
    data["pools"] = updated_pools


def apply_coin_pools(coin_definitions: dict, output_dir: Path, jar_path: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    model_data_map = build_model_data_map(coin_definitions)
    with zipfile.ZipFile(jar_path) as z:
        for filename, spec in MOB_COIN_SPECS.items():
            coin_definition = coin_definitions.get(spec["coin_id"])
            if coin_definition is None:
                raise KeyError(f"Missing coin definition for {spec['coin_id']}")

            target_path = output_dir / filename
            internal = f"data/minecraft/loot_table/entities/{Path(filename).stem}.json"
            if internal not in z.namelist():
                internal = f"data/minecraft/loot_table/entities/{filename}"
            if internal not in z.namelist():
                print(f"SKIP {filename}: no vanilla loot table found")
                continue

            data = json.loads(z.read(internal).decode("utf-8"))
            coin_pool = build_coin_pool(
                coin_definition,
                spec["coin_count"],
                custom_model_data=model_data_map[coin_definition["id"]],
            )
            upsert_coin_pool(data, coin_pool)

            with target_path.open("w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

            print(f"Updated {filename} with {coin_definition['id']}")


def main(resource_pack_only: bool = False) -> None:
    coin_definitions = load_coin_definitions(COIN_DIR)
    if not resource_pack_only:
        apply_coin_pools(coin_definitions, ROOT_LOOT_TABLES, JAR)
    commands_path = ROOT / "data" / "economiarpg" / "functions" / "generated_coin_commands.mcfunction"
    manifest_path = ROOT / "data" / "economiarpg" / "coins" / "manifest.json"
    write_give_commands(coin_definitions, commands_path)
    # write a help function that prints usage and the prepared give commands
    help_path = ROOT / "data" / "economiarpg" / "functions" / "help.mcfunction"
    write_help_function(coin_definitions, help_path)
    test_loot_path = ROOT / "data" / "economiarpg" / "loot_tables" / "test_bronze_coin.json"
    write_coin_test_loot_table(coin_definitions, test_loot_path)
    comparison_path = ROOT / "data" / "economiarpg" / "functions" / "compare_coin_items.mcfunction"
    write_coin_comparison_function(coin_definitions, comparison_path)
    trader_path = ROOT / "data" / "economiarpg" / "functions" / "spawn_coin_trader.mcfunction"
    write_villager_trader_function(coin_definitions, trader_path)
    write_coin_manifest(coin_definitions, manifest_path)
    write_resource_pack_assets(coin_definitions)
    write_resource_pack_zip(ASSETS_DIR, ROOT / "resource_pack.zip")
    print(f"Wrote {commands_path}")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate coin resources and optionally update loot tables.")
    parser.add_argument(
        "--resource-pack-only",
        action="store_true",
        help="Generate only the resource pack assets and zip without modifying loot tables.",
    )
    args = parser.parse_args()
    main(resource_pack_only=args.resource_pack_only)

