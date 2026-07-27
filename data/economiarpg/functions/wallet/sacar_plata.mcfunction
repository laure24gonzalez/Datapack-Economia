# Entrega una moneda de plata si el saldo lo permite.
execute if score @s economiarpg.money matches 10.. run give @s minecraft:iron_nugget[custom_data={economiarpg:{type:"coin",currency:"silver",value:10}},custom_name='{"text":"Moneda de Plata","color":"aqua","bold":true}',lore=['{"text":"Valor: 10","color":"gray"}'],rarity="rare"] 1
scoreboard players remove @s economiarpg.money 10
function economiarpg:wallet/refresh_sidebar
tellraw @s {"text":"✅ Se retiraron 10 de saldo como una moneda de plata.","color":"green"}
