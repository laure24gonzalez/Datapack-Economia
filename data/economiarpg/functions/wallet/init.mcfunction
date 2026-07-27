# Inicializa los scoreboards solo una vez para evitar errores al recargar el datapack.
execute unless score #economiarpg.init deathCount matches 1 run function economiarpg:wallet/init_once
execute if score #economiarpg.init deathCount matches 1 run function economiarpg:wallet/refresh_sidebar
