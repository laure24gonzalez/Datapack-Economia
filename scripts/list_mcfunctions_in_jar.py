import zipfile
JAR=r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"
with zipfile.ZipFile(JAR) as z:
    names=z.namelist()
    mcfn=[n for n in names if n.endswith('.mcfunction')]
    print('mcfunction count:', len(mcfn))
    for p in mcfn[:50]:
        print(p)
