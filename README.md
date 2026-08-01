# EconomiaRPG

## Nuevo enfoque: economía basada en objetos físicos

Se abandonó el sistema de wallet y los comandos simulados. La economía ahora se basa en objetos físicos personalizados que el jugador puede recoger, almacenar, intercambiar y convertir.

### Qué se mantiene activo

- Los loot tables de mobs siguen intactos.
- Los drops actuales de monedas no se modifican.
- La parte de monedas en loot tables sigue funcionando igual que antes.

### Estructura actual del datapack

- data/minecraft/loot_table/entities/ : loot tables de mobs, sin modificar.
- data/minecraft/tags/function/ : tags de carga y tick.
- data/economiarpg/function/ : funciones mínimas de carga y prueba.
- data/economiarpg/recipe/ : recetas de conversión entre monedas físicas.

### Objetos personalizados

La economía se organiza con tres niveles de objetos físicos:

1. Moneda
2. Lingote comercial
3. Bloque comercial

Conversiones:

- 9 monedas = 1 lingote comercial
- 9 lingotes comerciales = 1 bloque comercial
- 1 lingote comercial = 9 monedas
- 1 bloque comercial = 9 lingotes comerciales

### Identificación interna

Los objetos van a ser realmente personalizados mediante componentes de Minecraft 1.21.11, como `custom_data`.

Esto permite que:

- una pepita vanilla no funcione como moneda,
- un lingote vanilla no funcione como lingote comercial,
- un bloque vanilla no funcione como bloque comercial.

### Objetos previstos

- Pepita: "Pepita de moneda"
- Lingote: "Lingote de moneda"
- Bloque: "Bloque de moneda"

### Compatibilidad futura

La idea es dejar el sistema listo para que en el futuro pueda usarse con:

- resource pack,
- textos personalizados,
- lore,
- identificadores internos,
- recetas de intercambio,
- comerciantes,
- tiendas.

## Estado del proyecto

### Activo

- Loot tables de mobs
- Drops actuales de monedas
- Carga base del datapack
- Recetas de conversión físicas

### Obsoleto y retirado

- Sistema de wallet
- Funciones de saldo por comandos
- Comandos tipo `/dinero`, `/pagar`, `/billetera`, etc.

## Notas de diseño

- No se va a modificar el sistema de loot tables existente.
- No se van a cambiar los drops actuales.
- El sistema se mantiene limpio y orientado a objetos físicos.
- La economía podrá evolucionar hacia tiendas y comerciantes sin depender de scoreboards o comandos simulados.
