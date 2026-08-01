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
    ordered = sorted(coin_definitions.values(), key=lambda item: item["id"])
    return {coin["id"]: index for index, coin in enumerate(ordered, start=1)}


def build_coin_pool(coin_definition: dict, coin_count: int, custom_model_data: int | None = None) -> dict:
    lore_lines = coin_definition.get("lore") or [f"Valor: {coin_definition.get('value', 1)}"]
    lore_entries = [{"text": line, "color": "gray", "italic": False, "bold": True} for line in lore_lines]
    components = {
        "minecraft:custom_name": {
            "text": coin_definition.get("display_name", "Moneda"),
            "color": coin_definition.get("color", "white"),
            "bold": True,
        },
        "minecraft:lore": lore_entries,
        "minecraft:custom_data": {
            "economiarpg": {
                "type": "coin",
                "id": coin_definition["id"],
                "currency": coin_definition["currency"],
                "value": coin_definition["value"],
            }
        },
        "minecraft:rarity": coin_definition.get("rarity", "common"),
    }
    return {
        "rolls": 1.0,
        "bonus_rolls": 0.0,
        "conditions": [{"condition": "minecraft:killed_by_player"}],
        "entries": [{
            "type": "minecraft:item",
            "name": coin_definition["item"],
            "functions": [
                {"function": "minecraft:set_count", "count": coin_count},
                {"function": "minecraft:set_components", "components": components},
            ],
        }],
    }


def build_give_command(coin_definition: dict, count: int = 1, player: str = "@p", custom_model_data: int | None = None) -> str:
    custom_data_payload = "{" + ",".join([
        f'type:"{coin_definition["id"]}"' if False else ""
    ]) + "}"
    custom_data_snbt = (
        "{economiarpg:{type:\"coin\",id:\""
        + coin_definition["id"]
        + "\",currency:\""
        + coin_definition["currency"]
        + "\",value:"
        + str(coin_definition["value"])
        + "}}"
    )
    component_arguments = [f"custom_data={custom_data_snbt}"]
    if custom_model_data is not None:
        component_arguments.append(f"custom_model_data={custom_model_data}")
    component_string = ",".join(component_arguments)
    return f"give {player} {coin_definition['item']}[{component_string}] {count}"


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

    for base_item, matching_coins in grouped_by_item.items():
        base_model_path = ASSETS_DIR / "minecraft" / "models" / "item" / f"{base_item}.json"
        base_model_path.parent.mkdir(parents=True, exist_ok=True)
        primary_coin = sorted(matching_coins, key=lambda item: item["id"])[0]
        base_model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"economiarpg:item/{primary_coin['id']}"},
        }
        base_model_path.write_text(json.dumps(base_model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_resource_pack_zip(assets_dir: Path, output_zip: Path, pack_mcmeta_path: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "pack": {
            "pack_format": 75.0,
            "description": "EconomiaRPG",
        }
    }
    pack_mcmeta_path.write_text(json.dumps(manifest, ensure_ascii=False) + "\n", encoding="utf-8")

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
            coin_pool = build_coin_pool(coin_definition, spec["coin_count"])
            upsert_coin_pool(data, coin_pool)

            with target_path.open("w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

            print(f"Updated {filename} with {coin_definition['id']}")


def main() -> None:
    coin_definitions = load_coin_definitions(COIN_DIR)
    apply_coin_pools(coin_definitions, ROOT_LOOT_TABLES, JAR)
    commands_path = ROOT / "data" / "economiarpg" / "function" / "generated_coin_commands.mcfunction"
    manifest_path = ROOT / "data" / "economiarpg" / "coins" / "manifest.json"
    write_give_commands(coin_definitions, commands_path)
    write_coin_manifest(coin_definitions, manifest_path)
    write_resource_pack_assets(coin_definitions)
    write_resource_pack_zip(ASSETS_DIR, ROOT / "resource_pack.zip", ROOT / "pack.mcmeta")
    print(f"Wrote {commands_path}")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()

