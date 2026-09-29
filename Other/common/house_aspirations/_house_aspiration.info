# In admin realms powerful families give bonuses to the house and the liege
# Icon is automatically fetched based on key matching texture in HOUSE_POWER_BONUS_ICON_PATH
key = {
	# If a house aspiration should show in main HUD interface
	# Default: no
	show_in_main_hud = no

	# Who can access this power?
	# root: dynasty house
	is_shown = { ... }

	### Brief: is_default ( bool )
	# When switching to government type with this house aspiration, will auto-select this if 'yes'.
	# Otherwise will pick based on ai_score of their first level, tiebreaker will pick randomly of available.
	# 
	# Default is no
	#
	is_default = no

	# Power level.
	# There must always be at least one.
	level = {
		# Cost to set or upgrade this power to this level
		# (setting a power is the same as "upgrading" it to it's first initial level)
		# root - house head
		cost = { ... }

		# Modifiers that the top liege will receive if the family is powerful.
		powerful_family_top_liege_modifier = {}

		# Modifiers that every house member will receive if the family is powerful.
		powerful_family_member_modifier = {}

		# Modifiers that every house member will receive regardless.
		any_house_member_modifier = {}

		# Modifiers for house head
		house_head_modifier = {}

		# How much AI likes this power level
		# Used for initial power pick and to decide if upgrade current power or switch to a new one
		# root: house head
		ai_score = {}

		# Level "parameters" used to tag a level
		parameters = {}


		# Level "house_head_parameters" used for house head parameters. Doesn't check if character is house head.
		house_head_parameters = {}

		
		# Allows for requesting great project contributions from Allies when this level is active
		# Default: No
		#
		can_request_great_project_contributions_from_allies = no

		# Can upgrade to the next level?
		# root: character
		can_upgrade = {}
	}

	# Texture used in the house attribute window
	illustration = "path/to/image.dds"

	# After changing house aspiration, how many days before you can change again?
	# days/weeks/months/years = X
	cooldown = { days = 7 }

	# Runs any designated effects when changing TO this aspiration
	# root = <character>
	# scope:house = <house>
	on_changed = {
	}

	# root = <character>
	# scope:house = <house>
	on_upgraded = {
	}
}
