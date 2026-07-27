# Retiro básico: convierte saldo en monedas físicas de mayor valor cuando es posible.
execute if score @s economiarpg.money matches 100.. run function economiarpg:wallet/sacar_oro
execute unless score @s economiarpg.money matches 100.. if score @s economiarpg.money matches 10.. run function economiarpg:wallet/sacar_plata
execute unless score @s economiarpg.money matches 10.. if score @s economiarpg.money matches 1.. run function economiarpg:wallet/sacar_bronce
execute unless score @s economiarpg.money matches 1.. run tellraw @s {"text":"❌ No tienes saldo para retirar.","color":"red"}
