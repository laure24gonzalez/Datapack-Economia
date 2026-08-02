import zipfile
from pathlib import Path

JAR = r"c:\Users\laure\AppData\Roaming\.minecraft\versions\1.21.11\1.21.11.jar"

with zipfile.ZipFile(JAR) as z:
    names = z.namelist()

functions_paths = [n for n in names if '/functions/' in n]
function_paths = [n for n in names if '/function/' in n]

print('Count /functions/ in JAR:', len(functions_paths))
if len(functions_paths) > 0:
    print('Example /functions/ entries:')
    for p in functions_paths[:10]:
        print(' ', p)

print('\nCount /function/ in JAR:', len(function_paths))
if len(function_paths) > 0:
    print('Example /function/ entries:')
    for p in function_paths[:10]:
        print(' ', p)
