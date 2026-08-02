# Comandos y pasos de prueba para EconomiaRPG

Este archivo reúne los comandos y pasos que se han usado para verificar el datapack, el loot y el resource pack.

## 1. Activar el entorno virtual de Python
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Descripción: activa el entorno virtual del proyecto para ejecutar los scripts de generación y pruebas.

## 2. Regenerar los loot tables y los assets del resource pack
```powershell
python .\scripts\apply_mob_loot.py
```

Descripción: vuelve a generar:
- los loot tables de mobs
- los comandos de give de monedas
- el manifiesto de monedas
- los modelos y el ZIP del resource pack

## 3. Ejecutar las pruebas automáticas
```powershell
python -m unittest discover -s tests -v
```

Descripción: corre la suite de pruebas para comprobar que:
- los loot tables siguen generándose bien
- los modelos del resource pack se escriben correctamente
- el metadata del pack sigue siendo compatible

## 4. Verificar el contenido del ZIP del resource pack
```powershell
python -c "import zipfile; from pathlib import Path; root = Path(r'c:\Users\laure\AppData\Roaming\.minecraft\saves\Mundo nuevo\datapacks\EconomiaRPG'); z = zipfile.ZipFile(root / 'resource_pack.zip'); print('entries', len(z.namelist())); print('pack.mcmeta', 'pack.mcmeta' in z.namelist()); print('bronze texture', 'assets/economiarpg/textures/item/bronze_coin.png' in z.namelist())"
```

Descripción: comprueba que el ZIP del resource pack contiene los archivos esperados y que la textura está empaquetada.

## 5. Verificar el formato del PNG de la textura
```powershell
python -c "from pathlib import Path; p = Path(r'c:\Users\laure\AppData\Roaming\.minecraft\saves\Mundo nuevo\datapacks\EconomiaRPG\assets\economiarpg\textures\item\bronze_coin.png'); data = p.read_bytes(); print(data[:8]); print('size', len(data))"
```

Descripción: confirma que el archivo de textura es un PNG válido y que no está corrupto.

## 6. Probar el datapack en Minecraft
Pasos recomendados:
1. Recargar el datapack desde el mundo.
2. Recargar el resource pack desde la configuración del mundo.
3. Entrar al mundo y comprobar que los mobs sueltan monedas.
4. Verificar que las monedas muestran la textura personalizada.

## 7. Revisar los archivos generados
Rutas útiles:
- [data/minecraft/loot_table/entities](data/minecraft/loot_table/entities)
- [data/economiarpg/functions/generated_coin_commands.mcfunction](data/economiarpg/functions/generated_coin_commands.mcfunction)
- [resource_pack.zip](resource_pack.zip)
- [assets/economiarpg/textures/item](assets/economiarpg/textures/item)

## Resumen rápido
Si quieres una prueba rápida del flujo completo, ejecuta en este orden:
```powershell
.\.venv\Scripts\Activate.ps1
python .\scripts\apply_mob_loot.py
python -m unittest discover -s tests -v
```
