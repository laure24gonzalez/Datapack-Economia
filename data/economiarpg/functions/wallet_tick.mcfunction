scoreboard players enable @a economiarpg.wallet_cmd
scoreboard players operation @a economiarpg.wallet_sidebar = @a economiarpg.money
execute as @a[scores={economiarpg.wallet_cmd=1}] run function economiarpg:wallet/ver
execute as @a[scores={economiarpg.wallet_cmd=2}] run function economiarpg:wallet/guardar
execute as @a[scores={economiarpg.wallet_cmd=3}] run function economiarpg:wallet/sacar
execute as @a[scores={economiarpg.wallet_cmd=4}] run function economiarpg:wallet/pagar
scoreboard players set @a[scores={economiarpg.wallet_cmd=1..}] economiarpg.wallet_cmd 0
