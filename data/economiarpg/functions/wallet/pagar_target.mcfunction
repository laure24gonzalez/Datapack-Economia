# Pago a un jugador cercano.
execute if score @s economiarpg.money matches 10.. run scoreboard players remove @s economiarpg.money 10
execute if score @s economiarpg.money matches 10.. run scoreboard players add @a[tag=economiarpg.payer,limit=1] economiarpg.money 10
execute if score @s economiarpg.money matches 10.. run tellraw @s [{"text":"✅ Se pagaron 10 a ","color":"green"},{"selector":"@a[tag=economiarpg.payer,limit=1]","color":"yellow"}]
execute if score @s economiarpg.money matches 10.. run tellraw @a[tag=economiarpg.payer,limit=1] [{"text":"💰 Recibiste 10 de ","color":"gold"},{"selector":"@s","color":"yellow"}]
execute unless score @s economiarpg.money matches 10.. run tellraw @a[tag=economiarpg.payer,limit=1] [{"text":"❌ No tienes suficiente saldo para pagar a ","color":"red"},{"selector":"@s","color":"yellow"}]
function economiarpg:wallet/refresh_sidebar
