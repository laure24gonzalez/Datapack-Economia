# Función para spawnear un aldeano personalizado de tienda.
# No modifica los aldeanos vanilla existentes.
# Solo está pensada para que operadores la ejecuten manualmente.

summon villager ~ ~ ~ {VillagerData:{profession:"minecraft:armorer",type:"minecraft:plains"},CustomName:'{"text":"Tienda EconomiaRPG"}',Invulnerable:1b,NoAI:1b,Offers:{Recipes:[]}}
