# EconomiaRPG

## Arquitectura del sistema

Este datapack usa únicamente funciones de datapack vanilla y scoreboards permanentes. No se crean comandos personalizados reales ni plugins.

### Estructura base

- data/minecraft/tags/functions/
- data/lospibes/functions/
  - economia/
  - stats/
  - utils/

### Scoreboards permanentes

- pepitas: saldo principal del servidor.
- kills: cantidad de asesinatos del jugador.
- muertes: cantidad de veces que murió el jugador.
- playtime: tiempo jugado del jugador.
- nivel: progreso o nivel del jugador.
- pagar: trigger para iniciar un pago.
- saldo: trigger para consultar saldo.
- transferir: trigger para transferir dinero.
- lospibes.temp y lospibes.temp2: scoreboards internos temporales.

## Sistema de moneda: Pepitas

La moneda del servidor se llama Pepitas.

El saldo de cada jugador se guarda en el objective definitivo `economiarpg.money`.

Este objective es el que se usará para:
- sidebar personalizada,
- tiendas,
- misiones,
- recompensas,
- rangos,
- y futuras integraciones.

Ejemplo:
- Laure: `economiarpg.money = 1250`

### Funciones implementadas en la wallet actual

- consultar saldo
- agregar pepitas
- quitar pepitas
- transferir pepitas entre jugadores
- validar saldo suficiente
- evitar valores negativos
- mostrar mensajes claros

## Sistema de estadísticas

Los nombres de los objetivos son fijos y deben mantenerse así para compatibilidad futura con sidebar, misiones y tiendas:

- `kills`
- `muertes`
- `playtime`
- `nivel`

## Sistema de interacción compatible con datapack vanilla

Un datapack vanilla no puede registrar comandos propios como `/dinero`, `/pagar` o `/tienda`.

La forma compatible es:

1. Usar `/trigger` cuando sea posible.
2. Usar `/function` para acciones directas.
3. Usar libros, botones o menús interactivos si se quiere una experiencia más cómoda.

### Entrada recomendada

- `/function lospibes:economia/saldo`
- `/function lospibes:economia/pagar`
- `/function lospibes:economia/agregar_pepitas`
- `/function lospibes:economia/quitar_pepitas`
- `/trigger saldo`
- `/trigger pagar`

## Archivos principales

- data/lospibes/functions/load.mcfunction
- data/lospibes/functions/economia/crear_scoreboards.mcfunction
- data/lospibes/functions/economia/agregar_pepitas.mcfunction
- data/lospibes/functions/economia/quitar_pepitas.mcfunction
- data/lospibes/functions/economia/pagar.mcfunction
- data/lospibes/functions/economia/saldo.mcfunction
- data/lospibes/functions/stats/kills.mcfunction
- data/lospibes/functions/stats/playtime.mcfunction
- data/lospibes/functions/utils/mensajes.mcfunction
- data/lospibes/functions/utils/validaciones.mcfunction

## Notas de diseño

- No se usan comandos inexistentes ni plugins.
- Todo funciona como datapack vanilla.
- Se deja preparado para una sidebar futura.
- Los nombres de los scoreboards son permanentes y claros.

## Estilo corto y fácil de recordar

El flujo pensado para el jugador es muy simple:

- /function economiarpg:ver
- /function economiarpg:guardar
- /function economiarpg:sacar
- /function economiarpg:pagar

Si luego quisieras un comando tipo /billetera guardar, eso se haría desde un plugin o un servidor con comandos personalizados, no desde un datapack puro.

✅ Fase 3 - Comerciantes

Aldeanos modificados que acepten únicamente las monedas.

No usar esmeraldas.

✅ Fase 4 - Tiendas

Comprar:

Herramientas
Comida
Armaduras
Objetos especiales

Pagando con monedas.

✅ Fase 5 - Misiones

Las dejamos para después.

No implementarlas todavía.

✅ Fase 6 - Trabajos

También para más adelante.

Por ejemplo:

Minero
Leñador
Pescador
Cazador
✅ Fase 7 - Expansiones

Cuando todo funcione:

Banco con interfaz.
Cajeros automáticos.
Intereses.
Casas de subastas.
Recompensas diarias.
Jefes personalizados.
Eventos.
Economía entre jugadores.
Impuestos (si alguna vez te interesa).
Estadísticas.
Lo que cambiaría ahora

Después de todo lo que descubrimos con las loot tables y el sistema de monedas, yo reorganizaría el proyecto así:

Versión 1.0
✅ Monedas.
✅ Drops de mobs.
✅ Loot vanilla conservado.
✅ Banco.
✅ Comerciantes.
Versión 1.1
Misiones.
Versión 1.2
Trabajos.
Versión 1.3
Economía avanzada.