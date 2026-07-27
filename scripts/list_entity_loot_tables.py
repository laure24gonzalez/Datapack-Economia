import zipfile

jar = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"
with zipfile.ZipFile(jar) as z:
    names = [n for n in z.namelist() if n.startswith("data/minecraft/loot_table/entities/") and n.endswith(".json")]
    for n in sorted(names):
        print(n)
