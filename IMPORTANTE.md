# EconomiaRPG - Decisiones de Diseño

## Economía

Se utilizará un sistema de monedas físicas.

Cada moneda es un objeto personalizado con:

- Nombre personalizado.
- Lore.
- Rareza.
- Custom Data.

Las monedas utilizan `minecraft:custom_data` para ser identificadas por el datapack y evitar conflictos con objetos vanilla.

Formato:

```json
economiarpg:{
    type:"coin",
    currency:"bronze",
    value:1
}
```

---

## Monedas

| Moneda | Valor |
|---------|------:|
| Bronce | 1 |
| Plata | 10 |
| Oro | 100 |
| Esmeralda | 1.000 |
| Diamante | 10.000 |
| Netherite | 100.000 |
| Ruby | 1.000.000 |

---

## Loot Tables

Actualmente cada mob genera sus monedas mediante una loot table personalizada.

Objetivo futuro:

Crear una loot table independiente por moneda.

Ejemplo:

```
data/economiarpg/
└── loot_tables/
    └── coins/
        ├── bronze.json
        ├── silver.json
        ├── gold.json
        ├── emerald.json
        ├── diamond.json
        ├── netherite.json
        └── ruby.json
```

Todos los mobs deberán llamar estas loot tables.

Ventajas:

- Una única definición por moneda.
- Fácil mantenimiento.
- Cambios globales modificando un solo archivo.
- Evita duplicar cientos de líneas de JSON.

---

## Aldeanos

Los aldeanos utilizarán trades personalizados.

Cada tienda venderá una categoría distinta.

Ejemplos:

- Herrero
- Constructor
- Minero
- Alquimista
- Granjero
- Mascotas
- Objetos especiales

Los aldeanos deberán solicitar exactamente las mismas monedas que generan las loot tables.

Actualmente existe una diferencia de componentes entre las monedas obtenidas mediante loot tables y las utilizadas por los aldeanos.

Este problema deberá resolverse antes de crear todas las tiendas.

---

## Equipamiento Legendario

Las armaduras y herramientas podrán superar los límites vanilla.

Ejemplos:

- Protection X
- Sharpness X
- Efficiency X
- Fortune V
- Unbreaking X
- Mending VIII

Además podrán utilizar:

```
attribute_modifiers
```

para agregar atributos personalizados.

Ejemplo:

- Vida máxima.
- Armadura.
- Armadura resistente.
- Velocidad.
- Daño.

---

## Armadura de Netherite

La armadura legendaria otorga en total:

❤️ +20 puntos de vida
(10 corazones adicionales)

Distribución:

- Casco: +4
- Pechera: +8
- Pantalones: +4
- Botas: +4

---

## Armadura para Lobos

Se comprobó que `attribute_modifiers` funcionan sobre `minecraft:wolf_armor`.

Actualmente se utiliza:

- +40 puntos de vida
- Encantamientos personalizados

Queda pendiente investigar:

- Cambio de tamaño del lobo.
- Regeneración automática mediante datapack.
- Atributos adicionales.

---

## Resource Pack

El proyecto incluirá un Resource Pack propio.

Contendrá:

- Texturas de monedas.
- Texturas de jefes.
- Modelos personalizados.
- Objetos especiales.

---

## Arquitectura

Objetivo:

Mantener una única definición para cada recurso.

Ejemplo:

- Una definición por moneda.
- Una definición por jefe.
- Una definición por armadura.

Evitar duplicar información entre archivos.

---

## Filosofía del Proyecto

EconomiaRPG no busca ser únicamente un datapack de economía.

El objetivo es convertirse en un RPG completo que incluya:

- Economía.
- Tiendas.
- Objetos legendarios.
- Jefes.
- Mascotas.
- Equipamiento personalizado.
- Resource Pack.
- Progresión.