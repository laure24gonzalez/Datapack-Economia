scoreboard objectives add economiarpg.money dummy
scoreboard objectives add economiarpg.wallet_sidebar dummy
scoreboard objectives add economiarpg.temp dummy
scoreboard objectives add economiarpg.deposit dummy
scoreboard objectives add economiarpg.admin dummy
scoreboard objectives add economiarpg.init dummy
scoreboard objectives add economiarpg.wallet_cmd trigger

scoreboard players set #economiarpg.version economiarpg.temp 1
scoreboard players set #economiarpg.bronze_value economiarpg.temp 1
scoreboard players set #economiarpg.silver_value economiarpg.temp 10
scoreboard players set #economiarpg.gold_value economiarpg.temp 100

scoreboard objectives setdisplay sidebar economiarpg.wallet_sidebar
scoreboard objectives modify economiarpg.wallet_sidebar displayname {"text":"ECONOMIA RPG","color":"gold"}
scoreboard players enable @a economiarpg.wallet_cmd
scoreboard players set #economiarpg.init economiarpg.init 1
