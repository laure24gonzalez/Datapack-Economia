clear @p minecraft:copper_nugget
loot give @p loot minecraft:entities/zombie
give @p minecraft:copper_nugget{display:{Name:"{\"text\":\"Moneda de bronce\",\"color\":\"red\",\"bold\":true}",Lore:["{\"text\":\"Valor: 1\",\"color\":\"gray\",\"italic\":false,\"bold\":true}"]},minecraft:custom_data:{economiarpg:{type:"coin",id:"bronze_coin",currency:"bronze",value:1}},minecraft:rarity:"common",minecraft:custom_model_data:1} 1
tellraw @a {"text":"[EconomiaRPG] Compara el item de loot y el item de /give", "color":"light_purple"}
