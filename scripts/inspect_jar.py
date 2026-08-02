import zipfile
jar = r'c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar'
with zipfile.ZipFile(jar) as z:
    for name in ['pack.mcmeta', 'data/minecraft/tags/function/load.json', 'data/minecraft/tags/function/tick.json']:
        print(name)
        print(z.read(name).decode('utf-8'))
        print('---')
