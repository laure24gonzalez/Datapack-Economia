# Transfiere dinero del ejecutor a otro jugador.
# Se usa así:
# /scoreboard players set #economiarpg.target economiarpg.temp <id>
# /scoreboard players set #economiarpg.input economiarpg.temp 50
# /function economiarpg:wallet/transferir

execute if score #economiarpg.input economiarpg.temp matches 1.. if score @s economiarpg.money >= #economiarpg.input economiarpg.temp if entity @a[scores={economiarpg.money=0..}] run function economiarpg:wallet/transferir_target
execute unless score #economiarpg.input economiarpg.temp matches 1.. run tellraw @s {"text":"❌ Debes indicar una cantidad mayor que 0.","color":"red"}
execute if score #economiarpg.input economiarpg.temp matches 1.. unless score @s economiarpg.money >= #economiarpg.input economiarpg.temp run tellraw @s {"text":"❌ No tienes suficiente dinero.","color":"red"}

scoreboard players set #economiarpg.input economiarpg.temp 0
scoreboard players set #economiarpg.target economiarpg.temp 0
function economiarpg:wallet/refresh_sidebar
