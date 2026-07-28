# Muestra el saldo del jugador ejecutor.
tellraw @s [{"text":"Saldo: ","color":"gold"},{"score":{"name":"@s","objective":"dinero"},"color":"yellow"},{"text":" de dinero","color":"gold"}]
