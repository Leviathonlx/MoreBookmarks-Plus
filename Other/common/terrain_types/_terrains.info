key = {
	movement_speed = 1		# Speed on this type of terrain
	attacker_modifier = {} # Modifiers for the attackers in a combat. See note on allowed modifiers below.
	defender_modifier = {} # Modifiers for the defender in a combat. See note on allowed modifiers below.
	attacker_combat_effects = {} # Combat effect for the attackers. Look for common/combat_effects/_combat_effects.info for more information on how script this one.
	defender_combat_effects = {} # Combat effect for the attackers. Look for common/combat_effects/_combat_effects.info for more information on how script this one.
	color = { r g b }		# Terrain color for the terrain type map mode
	combat_width = 1		# Multiplier on the combat width
	audio_parameter = 0		# Used to check the audio to play
	province_modifier = {}	# Modifier applied to the province. See note on allowed modifiers below.
	county_capital_modifier = {} # Modifier applied to the province if it is the county capital. See note on allowed modifiers below.
	travel_danger_score = 0 # The amount of danger this terrain provides when travelling over it.
	travel_danger_color = 0 # Terrain color for the travel planner map mode if the danger score is higher than the player's safety.
	provision_cost = 0		# The amount of provison cost for this terrain type when moving your domicile
	county_fertility = 0 	# The amount of Fertility contributed by this terrain type. Used to calculate Base County Fertility for relevant counties
	entity = "forest_birds_01" # Environmental graphical asset shown in this terrain.

Allowed Modifiers
=================

Modifiers referenced by a terrain object can be only generic (hardcoded) modifiers, or modifiers generated from the following databases:
- schemes
- holdings
- lifestyles
- regions

Other generated modifiers are _not_ allowed, such as those from other terrains, men_at_arms_types, cultures, or governments.

Generated Modifiers
===================

Each terrain type adds this modifiers automatically:

KEY + _attrition_mult = 0 			# Multiplier applied to attition of the terrain terrain type
KEY + _cancel_negative_supply = yes	# Discards supply penalties from the terrain type
KEY + _advantage = 0				# Advantage during the combat
KEY + _development_growth = 0.2		# Development growth if capital of a county is this terrain
KEY + _development_growth_factor = 0.2		# Development growth factor if capital of a county is this terrain
KEY + _construction_gold_cost = 0.2
KEY + _holding_construction_gold_cost = 0.2
KEY + _construction_piety_cost = 0.2
KEY + _holding_construction_piety_cost = 0.2
KEY + _construction_prestige_cost = 0.2
KEY + _holding_construction_prestige_cost = 0.2
KEY + _supply_limit = 200
KEY + _supply_limit_mult = 0.2
KEY + _tax_mult = 0.2
KEY + _levy_size = 0.2
KEY + _min_combat_roll = 0.2
KEY + _max_combat_roll = 0.2
KEY + _travel_danger = 0.2
KEY + _provision_use_mult = 0.2
