import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_mob_loot.py"


def main() -> None:
    print("Generating resource pack assets without modifying loot tables...")
    subprocess.run([sys.executable, str(SCRIPT), "--resource-pack-only"], check=True)
    print(f"Resource pack generated at: {ROOT / 'resource_pack.zip'}")
    print("Copy the ZIP to your Minecraft resourcepacks folder or use it directly from the datapack.")


if __name__ == "__main__":
    main()
