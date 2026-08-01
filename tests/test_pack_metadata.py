import json
import zipfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackMetadataTests(unittest.TestCase):
    def test_datapack_pack_format_matches_minecraft_1_21_11(self):
        pack_mcmeta = json.loads((ROOT / "pack.mcmeta").read_text(encoding="utf-8"))

        self.assertEqual(pack_mcmeta["pack"]["pack_format"], 75.0)

    def test_resource_pack_zip_uses_resource_pack_format_for_minecraft_1_21_11(self):
        with zipfile.ZipFile(ROOT / "resource_pack.zip") as archive:
            pack_mcmeta = json.loads(archive.read("pack.mcmeta"))

        self.assertEqual(pack_mcmeta["pack"]["pack_format"], 75.0)


if __name__ == "__main__":
    unittest.main()
