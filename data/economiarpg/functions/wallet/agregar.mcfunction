# Añade dinero al jugador ejecutor.
# Se usa así:
# /scoreboard players set #economiarpg.input economiarpg.temp 100
# /function economiarpg:wallet/agregar

execute if score #economiarpg.input economiarpg.temp matches 1.. run scoreboard players operation @s economiarpg.money += #economiarpg.input economiarpg.temp
execute if score #economiarpg.input economiarpg.temp matches 1.. run tellraw @s [{"text":"✅ Se añadieron ","color":"green"},{"score":{"name":"#economiarpg.input","objective":"economiarpg.temp"},"color":"yellow"},{"text":" de dinero a tu saldo.","color":"green"}]
execute unless score #economiarpg.input economiarpg.temp matches 1.. run tellraw @s {"text":"❌ Debes indicar una cantidad mayor que 0.","color":"red"}

scoreboard players set #economiarpg.input economiarpg.temp 0
function economiarpg:wallet/refresh_sidebar
