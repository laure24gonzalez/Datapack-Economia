# Entrega una moneda de oro si el saldo lo permite.
execute if score @s economiarpg.money matches 100.. run give @s minecraft:gold_nugget[custom_data={economiarpg:{type:"coin",currency:"gold",value:100}},custom_name='{"text":"Moneda de Oro","color":"gold","bold":true}',lore=['{"text":"Valor: 100","color":"gray"}'],rarity="epic"] 1
scoreboard players remove @s economiarpg.money 100
function economiarpg:wallet/refresh_sidebar
tellraw @s {"text":"✅ Se retiraron 100 de saldo como una moneda de oro.","color":"green"}
