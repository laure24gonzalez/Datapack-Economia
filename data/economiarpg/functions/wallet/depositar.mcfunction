# Deposita monedas físicas del inventario al saldo virtual.
scoreboard players set @s economiarpg.deposit 0
scoreboard players set @s economiarpg.temp 0

# Bronce
# Usamos clear con count 0 como contador para saber cuántas monedas coinciden sin borrar aún el inventario.
execute store result score @s economiarpg.temp run clear @s minecraft:copper_nugget[custom_data={economiarpg:{type:"coin",currency:"bronze",value:1}}] 0
scoreboard players operation @s economiarpg.deposit += @s economiarpg.temp
execute if score @s economiarpg.temp matches 1.. run clear @s minecraft:copper_nugget[custom_data={economiarpg:{type:"coin",currency:"bronze",value:1}}]
execute if score @s economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.temp *= #economiarpg.bronze_value economiarpg.temp
execute if score @s economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.money += @s economiarpg.temp

# Plata
scoreboard players set @s economiarpg.temp 0
execute store result score @s economiarpg.temp run clear @s minecraft:iron_nugget[custom_data={economiarpg:{type:"coin",currency:"silver",value:10}}] 0
scoreboard players operation @s economiarpg.deposit += @s economiarpg.temp
execute if score @s economiarpg.temp matches 1.. run clear @s minecraft:iron_nugget[custom_data={economiarpg:{type:"coin",currency:"silver",value:10}}]
execute if score @s economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.temp *= #economiarpg.silver_value economiarpg.temp
execute if score @s economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.money += @s economiarpg.temp

# Oro
scoreboard players set @s economiarpg.temp 0
execute store result score @s economiarpg.temp run clear @s minecraft:gold_nugget[custom_data={economiarpg:{type:"coin",currency:"gold",value:100}}] 0
scoreboard players operation @s economiarpg.deposit += @s economiarpg.temp
execute if score @s economiarpg.temp matches 1.. run clear @s minecraft:gold_nugget[custom_data={economiarpg:{type:"coin",currency:"gold",value:100}}]
execute if score @s economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.temp *= #economiarpg.gold_value economiarpg.temp
execute if score @s economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.money += @s economiarpg.temp

execute if score @s economiarpg.deposit matches 1.. run tellraw @s [{"text":"✔ Dinero guardado correctamente.\n","color":"green"},{"text":"+$","color":"gold"},{"score":{"name":"@s","objective":"economiarpg.money"},"color":"yellow"}]
execute unless score @s economiarpg.deposit matches 1.. run tellraw @s {"text":"❌ No tienes monedas para depositar.","color":"red"}
function economiarpg:wallet/refresh_sidebar
