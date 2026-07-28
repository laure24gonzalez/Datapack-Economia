# Quita dinero al jugador ejecutor si tiene saldo suficiente.
# Se usa así:
# /scoreboard players set #economiarpg.input economiarpg.temp 50
# /function economiarpg:wallet/quitar

execute if score #economiarpg.input economiarpg.temp matches 1.. if score @s economiarpg.money >= #economiarpg.input economiarpg.temp run scoreboard players operation @s economiarpg.money -= #economiarpg.input economiarpg.temp
execute if score #economiarpg.input economiarpg.temp matches 1.. if score @s economiarpg.money >= #economiarpg.input economiarpg.temp run tellraw @s [{"text":"✅ Se quitaron ","color":"green"},{"score":{"name":"#economiarpg.input","objective":"economiarpg.temp"},"color":"yellow"},{"text":" de dinero de tu saldo.","color":"green"}]
execute if score #economiarpg.input economiarpg.temp matches 1.. unless score @s economiarpg.money >= #economiarpg.input economiarpg.temp run tellraw @s {"text":"❌ No tienes suficiente dinero.","color":"red"}
execute unless score #economiarpg.input economiarpg.temp matches 1.. run tellraw @s {"text":"❌ Debes indicar una cantidad mayor que 0.","color":"red"}

scoreboard players set #economiarpg.input economiarpg.temp 0
function economiarpg:wallet/refresh_sidebar
