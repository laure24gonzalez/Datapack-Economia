# Transferencia simple entre jugadores usando trigger y un selector objetivo.
# El jugador ejecutor debe haber fijado el trigger con un valor que indique la cantidad.
# Ejemplo: /trigger pagar set 100
# El objetivo se define manualmente desde el sistema futuro.

execute as @s[scores={pagar=1..}] run scoreboard players operation @s lospibes.temp = @s pagar
execute as @s[scores={pagar=1..}] run scoreboard players operation @s lospibes.temp2 = @s dinero
execute as @s[scores={pagar=1..}] if score @s lospibes.temp <= @s lospibes.temp2 run scoreboard players remove @s dinero 0
execute as @s[scores={pagar=1..}] run tellraw @s {"text":"Pago procesado.","color":"green"}
scoreboard players set @s[scores={pagar=1..}] pagar 0
