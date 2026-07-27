# Pago básico: envía 10 de saldo al jugador más cercano dentro de 6 bloques.
tag @s add economiarpg.payer
execute as @a[distance=..6,limit=1,sort=nearest] unless entity @s[tag=economiarpg.payer] run function economiarpg:wallet/pagar_target
execute if entity @s[tag=economiarpg.payer] unless entity @a[distance=..6,limit=1,sort=nearest,tag=!economiarpg.payer] run tellraw @s {"text":"❌ No hay otro jugador cerca para pagar.","color":"red"}
tag @s remove economiarpg.payer
