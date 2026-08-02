# Compare la moneda generada por loot con la moneda generada por /give
clear @p
loot give @p loot economiarpg:test_bronze_coin
give @p minecraft:copper_nugget{display:{Name:'{\"text\": \"Moneda de bronce\", \"color\": \"red\", \"bold\": true}',Lore:['{\"text\": \"Valor: 1\", \"color\": \"gray\", \"italic\": false, \"bold\": true}']},minecraft:custom_data:{economiarpg:{type:"coin",id:"bronze_coin",currency:"bronze",value:1}},rarity:"common",CustomModelData:1} 1
tellraw @a {"text":"Selecciona cada item y ejecuta /data get entity @p SelectedItem para comparar el NBT.","color":"yellow"}
tellraw @a {"text":"La primera moneda es la de loot table y la segunda es la moneda creada con /give.","color":"gold"}
