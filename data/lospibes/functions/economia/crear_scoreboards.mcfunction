# Scoreboards permanentes del sistema de economía y estadísticas.
scoreboard objectives add dinero dummy {"text":"Dinero","color":"gold"}
scoreboard objectives add kills playerKillCount {"text":"Kills","color":"green"}
scoreboard objectives add muertes deathCount {"text":"Muertes","color":"red"}
scoreboard objectives add playtime minecraft.custom:minecraft.play_time {"text":"Playtime","color":"aqua"}
scoreboard objectives add nivel dummy {"text":"Nivel","color":"yellow"}

# Trigger para acciones del jugador.
scoreboard objectives add pagar trigger
scoreboard objectives add saldo trigger
scoreboard objectives add transferir trigger

# Scoreboards temporales internos.
scoreboard objectives add lospibes.temp dummy
scoreboard objectives add lospibes.temp2 dummy
