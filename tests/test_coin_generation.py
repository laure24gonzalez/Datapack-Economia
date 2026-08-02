import importlib.util
import json
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("apply_mob_loot", ROOT / "scripts" / "apply_mob_loot.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CoinGenerationTests(unittest.TestCase):
    def test_load_coin_definitions_reads_json_with_ids(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")

        self.assertIn("bronze_coin", definitions)
        self.assertEqual(definitions["bronze_coin"]["currency"], "bronze")
        self.assertEqual(definitions["bronze_coin"]["item"], "minecraft:copper_nugget")

    def test_build_coin_pool_uses_definition_fields(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        pool = MODULE.build_coin_pool(definitions["bronze_coin"], 3)

        self.assertEqual(pool["entries"][0]["name"], "minecraft:copper_nugget")
        self.assertEqual(pool["entries"][0]["functions"][0]["function"], "minecraft:set_count")
        self.assertEqual(pool["entries"][0]["functions"][0]["count"], 3)
        self.assertIn("minecraft:set_components", [function["function"] for function in pool["entries"][0]["functions"]])
        components_function = next(function for function in pool["entries"][0]["functions"] if function.get("function") == "minecraft:set_components")
        components = components_function["components"]
        self.assertIn("minecraft:custom_name", components)
        self.assertIn("minecraft:lore", components)
        self.assertIn("minecraft:custom_data", components)
        self.assertIn("minecraft:rarity", components)

    def test_build_give_command_contains_coin_metadata(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        command = MODULE.build_give_command(definitions["bronze_coin"], count=3, custom_model_data=1)

        self.assertIn("give @p minecraft:copper_nugget{", command)
        self.assertIn("bronze_coin", command)
        self.assertIn("economiarpg", command)
        self.assertIn("CustomModelData:1", command)

    def test_build_coin_pool_includes_component_metadata_for_loot(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        pool = MODULE.build_coin_pool(definitions["bronze_coin"], 2, custom_model_data=1)

        function_names = [function.get("function") for function in pool["entries"][0]["functions"]]
        self.assertIn("minecraft:set_components", function_names)

        components_function = next(function for function in pool["entries"][0]["functions"] if function.get("function") == "minecraft:set_components")
        self.assertEqual(components_function["components"]["minecraft:rarity"], "common")
        self.assertIn("economiarpg", str(components_function["components"]["minecraft:custom_data"]))

    def test_build_coin_item_tag_includes_loot_and_display_components(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        item_tag = MODULE.build_coin_item_tag(definitions["bronze_coin"], custom_model_data=1)

        self.assertIn("minecraft:custom_data:{economiarpg:{type:\"coin\",id:\"bronze_coin\",currency:\"bronze\",value:1}}", item_tag)
        self.assertIn("CustomModelData:1", item_tag)
        self.assertIn("display:{Name:'{\\\"text\\\": \\\"Moneda de bronce\\\", \\\"color\\\": \\\"red\\\", \\\"bold\\\": true}',Lore:[", item_tag)

    def test_write_coin_comparison_function_writes_compare_flow(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        compare_path = ROOT / "data" / "economiarpg" / "function" / "compare_coin_items.mcfunction"
        MODULE.write_coin_comparison_function(definitions, compare_path)

        self.assertTrue(compare_path.exists())
        content = compare_path.read_text(encoding="utf-8")
        self.assertIn("loot give @p loot economiarpg:test_bronze_coin", content)
        self.assertIn("give @p minecraft:copper_nugget", content)
        self.assertIn("/data get entity @p SelectedItem", content)

    def test_write_coin_test_loot_table_creates_loot_table_file(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        test_loot_path = ROOT / "data" / "economiarpg" / "loot_tables" / "test_bronze_coin.json"
        MODULE.write_coin_test_loot_table(definitions, test_loot_path)

        self.assertTrue(test_loot_path.exists())
        loot_contents = json.loads(test_loot_path.read_text(encoding="utf-8"))
        self.assertEqual(loot_contents.get("type"), "minecraft:generic")
        self.assertEqual(len(loot_contents.get("pools", [])), 1)
        self.assertEqual(loot_contents["pools"][0]["entries"][0]["name"], "minecraft:copper_nugget")

    def test_write_resource_pack_assets_uses_direct_texture_for_base_item_models(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        MODULE.write_resource_pack_assets(definitions)

        copper_model_path = ROOT / "assets" / "minecraft" / "models" / "item" / "copper_nugget.json"
        self.assertTrue(copper_model_path.exists(), f"Expected override model at {copper_model_path}")

        copper_model = copper_model_path.read_text(encoding="utf-8")
        self.assertIn('"layer0": "minecraft:item/copper_nugget"', copper_model)
        self.assertIn('"overrides"', copper_model)
        self.assertIn('"custom_model_data": 1', copper_model)

    def test_write_resource_pack_zip_contains_latest_generated_assets(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        MODULE.write_resource_pack_assets(definitions)
        MODULE.write_resource_pack_zip(ROOT / "assets", ROOT / "resource_pack.zip", ROOT / "pack.mcmeta")

        with zipfile.ZipFile(ROOT / "resource_pack.zip") as archive:
            self.assertIn("assets/minecraft/models/item/copper_nugget.json", archive.namelist())
            self.assertIn("assets/economiarpg/textures/item/bronze_coin.png", archive.namelist())
            copper_model = archive.read("assets/minecraft/models/item/copper_nugget.json").decode("utf-8")
        # The zip should include the generated copper model with vanilla base texture
        # and overrides that point to the economiarpg coin models.
        self.assertIn('"layer0": "minecraft:item/copper_nugget"', copper_model)
        self.assertIn('"overrides"', copper_model)
        self.assertIn('"custom_model_data": 1', copper_model)

    def test_root_loot_table_path_uses_singular_directory(self):
        self.assertEqual(MODULE.ROOT_LOOT_TABLES.name, "entities")
        self.assertEqual(MODULE.ROOT_LOOT_TABLES.parent.name, "loot_table")

    def test_workspace_zombie_loot_table_contains_coin_entry(self):
        zombie_loot_path = ROOT / "data" / "minecraft" / "loot_table" / "entities" / "zombie.json"
        self.assertTrue(zombie_loot_path.exists(), f"Expected loot table at {zombie_loot_path}")

        loot_contents = json.loads(zombie_loot_path.read_text(encoding="utf-8"))
        coin_entry_names = [
            entry.get("name")
            for pool in loot_contents.get("pools", [])
            for entry in pool.get("entries", [])
        ]

        self.assertIn("minecraft:copper_nugget", coin_entry_names)

    def test_workspace_zombie_loot_table_uses_component_lore(self):
        zombie_loot_path = ROOT / "data" / "minecraft" / "loot_table" / "entities" / "zombie.json"
        loot_contents = json.loads(zombie_loot_path.read_text(encoding="utf-8"))

        coin_entry = next(
            entry
            for pool in loot_contents.get("pools", [])
            for entry in pool.get("entries", [])
            if entry.get("name") == "minecraft:copper_nugget"
        )

        component_functions = [
            fn for fn in coin_entry.get("functions", [])
            if fn.get("function") == "minecraft:set_components"
        ]
        self.assertTrue(component_functions, "Expected a set_components function for the zombie coin entry")

        components = component_functions[0].get("components", {})
        self.assertIn("minecraft:custom_name", components)
        self.assertIn("minecraft:lore", components)
        self.assertIn("minecraft:custom_data", components)
        self.assertIn("minecraft:rarity", components)

if __name__ == "__main__":
    unittest.main()
