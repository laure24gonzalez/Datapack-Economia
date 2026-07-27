# Entrega una moneda de bronce si el saldo lo permite.
execute if score @s economiarpg.money matches 1.. run give @s minecraft:copper_nugget[custom_data={economiarpg:{type:"coin",currency:"bronze",value:1}},custom_name='{"text":"Moneda de Bronce","color":"red","bold":true}',lore=['{"text":"Valor: 1","color":"gray"}'],rarity="common"] 1
scoreboard players remove @s economiarpg.money 1
function economiarpg:wallet/refresh_sidebar
tellraw @s {"text":"✅ Se retiraron 1 de saldo como una moneda de bronce.","color":"green"}
