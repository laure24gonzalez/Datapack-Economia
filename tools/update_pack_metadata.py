import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root = ROOT

pack_mcmeta = {
    "pack": {
        "pack_format": 94.1,
        "description": "EconomiaRPG",
    }
}

(root / "pack.mcmeta").write_text(json.dumps(pack_mcmeta, ensure_ascii=False), encoding="utf-8")

zip_path = ROOT / "resource_pack.zip"
temp_path = ROOT / "resource_pack_tmp.zip"

if zip_path.exists():
    with zipfile.ZipFile(zip_path, "r") as zf:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as out:
            for name in zf.namelist():
                data = zf.read(name)
                if name == "pack.mcmeta":
                    resource_pack_mcmeta = json.loads(data.decode("utf-8-sig"))
                    resource_pack_mcmeta["pack"]["pack_format"] = 75.0
                    resource_pack_mcmeta["pack"]["description"] = "EconomiaRPG"
                    out.writestr(name, json.dumps(resource_pack_mcmeta, ensure_ascii=False))
                else:
                    out.writestr(name, data)

    if zip_path.exists():
        zip_path.unlink()
    temp_path.replace(zip_path)

print("Updated pack.mcmeta and resource_pack.zip")
