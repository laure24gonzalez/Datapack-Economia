# Refactor del sistema de monedas - EconomiaRPG

## Objetivo

Rediseñar completamente el sistema de monedas para que exista una única definición oficial de cada moneda.

Actualmente el script genera correctamente las loot tables de todos los mobs utilizando un diccionario (`mob_specs`), pero las monedas ahora también serán utilizadas por:

- Loot Tables
- Aldeanos
- Comandos /give
- Resource Pack
- Tiendas
- Banco
- Funciones del datapack
- Futuro mod Fabric

Por este motivo ya no es suficiente almacenar únicamente:

- coin_name
- coin_count
- name_text
- color
- rarity
- currency
- value

---

## Nuevo objetivo

Cada moneda deberá tener un identificador único y permanente.

Ejemplo:

```python
{
    "id": "bronze_coin",
    "item": "minecraft:copper_nugget",
    "display_name": "Moneda de bronce",
    "currency": "bronze",
    "value": 1,
    "rarity": "common",
    "color": "red",
    "lore": [
        "Valor: 1"
    ],
    "item_model": "economiarpg:bronze_coin"
}
```

Ese ID nunca deberá cambiar.

Aunque cambien:

- nombre
- textura
- valor
- rareza
- lore

---

## El script debe generar automáticamente

A partir de una única definición por moneda, generar:

- Loot Tables
- Comandos /give
- Objetos para aldeanos
- Definiciones para Resource Pack
- Documentación (opcional)

---

## Resource Pack

Cada moneda tendrá una textura independiente.

No se utilizarán distintos ítems vanilla.

Todas seguirán utilizando nuggets.

La diferencia visual deberá realizarse mediante:

- item_model
- modelo personalizado
- resource pack

No deberán afectar los nuggets vanilla.

---

## Compatibilidad con aldeanos

Los aldeanos deberán aceptar exactamente las mismas monedas que generan las loot tables. (sin afectar el tradeo vanilla de los mismos, se podran spawnear mediante items especiales o comandos de operador)

No deberán existir diferencias entre:

- moneda creada por loot table
- moneda creada por /give
- moneda utilizada en trades

Toda la información deberá provenir de la misma definición.

---

## Organización propuesta

Crear una carpeta:

economiarpg/

    coins/

        bronze.json

        silver.json

        gold.json

        emerald.json

        diamond.json

        netherite.json

        ruby.json

Cada archivo representa la definición oficial de una moneda.

El script de Python deberá leer estos archivos y generar automáticamente todo el contenido necesario.

---

## Objetivos del refactor

✔ Una sola fuente de verdad para todas las monedas.

✔ Evitar duplicar información.

✔ Facilitar cambios futuros.

✔ Compatibilidad completa con Resource Pack.

✔ Compatibilidad completa con aldeanos.

✔ Facilitar la incorporación de nuevas monedas.

✔ Mantener el proyecto escalable.