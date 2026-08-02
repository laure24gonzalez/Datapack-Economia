import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "economiarpg" / "shops" / "catalog.json"
OUTPUT_PATH = ROOT / "data" / "economiarpg" / "functions" / "villagers" / "shop_catalog_generated.mcfunction"

with CATALOG_PATH.open(encoding="utf-8") as fh:
    catalog = json.load(fh)

lines = ["# Generated shop catalog for EconomiaRPG"]
for shop_id, shop in catalog.get("shops", {}).items():
    lines.append(f"# Shop: {shop['name']}")
    for offer in shop.get("offers", []):
        price = offer["price"]
        lines.append(f"# {offer['id']} -> {price['amount']} {price['coin_id']}")

OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT_PATH}")
