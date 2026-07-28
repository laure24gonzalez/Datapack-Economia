# Validaciones base para economía.
# Evita valores negativos.
execute as @s[scores={dinero=..-1}] run scoreboard players set @s dinero 0
