import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_PACK_ZIP = ROOT / "resource_pack.zip"
TARGET_RESOURCEPACK_DIR = Path.home() / "AppData" / "Roaming" / ".minecraft" / "resourcepacks"
TARGET_RESOURCEPACK_ZIP = TARGET_RESOURCEPACK_DIR / "EconomiaRPG.zip"
SCRIPT = ROOT / "scripts" / "apply_mob_loot.py"


def main() -> None:
    print(f"Generating resource pack from {SCRIPT}")
    subprocess.run([sys.executable, str(SCRIPT)], check=True)

    if not RESOURCE_PACK_ZIP.exists():
        raise FileNotFoundError(f"Resource pack zip not found: {RESOURCE_PACK_ZIP}")

    TARGET_RESOURCEPACK_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RESOURCE_PACK_ZIP, TARGET_RESOURCEPACK_ZIP)
    print(f"Copied resource pack to: {TARGET_RESOURCEPACK_ZIP}")
    print("Enable 'EconomiaRPG' in Minecraft resource packs and reload the world.")


if __name__ == "__main__":
    main()
