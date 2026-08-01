import importlib.util
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
        self.assertEqual(pool["entries"][0]["functions"][1]["function"], "minecraft:set_components")
        self.assertIn("minecraft:custom_name", pool["entries"][0]["functions"][1]["components"])

    def test_build_give_command_contains_coin_metadata(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        command = MODULE.build_give_command(definitions["bronze_coin"], count=3, custom_model_data=1)

        self.assertIn("give @p minecraft:copper_nugget[", command)
        self.assertIn("bronze_coin", command)
        self.assertIn("custom_data=", command)
        self.assertIn("custom_model_data=1", command)

    def test_write_resource_pack_assets_uses_direct_texture_for_base_item_models(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        MODULE.write_resource_pack_assets(definitions)

        copper_model_path = ROOT / "assets" / "minecraft" / "models" / "item" / "copper_nugget.json"
        self.assertTrue(copper_model_path.exists(), f"Expected override model at {copper_model_path}")

        copper_model = copper_model_path.read_text(encoding="utf-8")
        self.assertIn('"layer0": "economiarpg:item/bronze_coin"', copper_model)
        self.assertNotIn('"overrides"', copper_model)

    def test_write_resource_pack_zip_contains_latest_generated_assets(self):
        definitions = MODULE.load_coin_definitions(ROOT / "data" / "economiarpg" / "coins")
        MODULE.write_resource_pack_assets(definitions)
        MODULE.write_resource_pack_zip(ROOT / "assets", ROOT / "resource_pack.zip", ROOT / "pack.mcmeta")

        with zipfile.ZipFile(ROOT / "resource_pack.zip") as archive:
            self.assertIn("assets/minecraft/models/item/copper_nugget.json", archive.namelist())
            self.assertIn("assets/economiarpg/textures/item/bronze_coin.png", archive.namelist())
            copper_model = archive.read("assets/minecraft/models/item/copper_nugget.json").decode("utf-8")

        self.assertIn('"layer0": "economiarpg:item/bronze_coin"', copper_model)

    def test_root_loot_table_path_uses_plural_directory(self):
        self.assertEqual(MODULE.ROOT_LOOT_TABLES.name, "entities")

if __name__ == "__main__":
    unittest.main()
