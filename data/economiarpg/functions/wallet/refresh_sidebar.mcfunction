scoreboard objectives remove economiarpg.wallet_sidebar
scoreboard objectives add economiarpg.wallet_sidebar dummy {"text":"ECONOMIA RPG","color":"gold"}
scoreboard players operation @a economiarpg.wallet_sidebar = @a economiarpg.money
scoreboard objectives setdisplay sidebar economiarpg.wallet_sidebar
