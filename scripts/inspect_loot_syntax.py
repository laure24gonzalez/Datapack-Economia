import zipfile

jar = r'c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar'
with zipfile.ZipFile(jar) as z:
    names = [n for n in z.namelist() if n.endswith('.json') and ('loot_table' in n or 'loot_function' in n or 'loot_condition' in n)]
    for name in names:
        try:
            text = z.read(name).decode('utf-8')
        except Exception:
            continue
        if 'set_components' in text or 'set_custom_data' in text or 'set_name' in text or 'set_lore' in text:
            print('---', name)
            for line in text.splitlines():
                if 'set_components' in line or 'set_custom_data' in line or 'set_name' in line or 'set_lore' in line or 'custom_name' in line or 'custom_data' in line:
                    print(line[:400])
            print()
