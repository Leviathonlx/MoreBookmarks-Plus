# Intents, can be used by multiple different activity types for more general intents
# Optionally support a target character, if a target trigger is defined they must pick a target when used
befriend = {
	# root = character picking this intent
	# scope:magnificence = the magnificence level of the activity
	# scope:special_option = the selected special option of the activity (if present)
	is_shown = {

	}
	
	# root = character picking this intent
	# scope:magnificence = the magnificence level of the activity
	# scope:special_option = the selected special option of the activity (if present)
	is_valid = {

	}

	# root = character picking this intent
	# scope:target = character that is the target
	# scope:special_option = the selected special option of the activity (if present)
	is_target_valid = {

	}

	# root = character who picked this intent
	on_invalidated = {

	}

	# root = character picking this intent
	# scope:target = character that is the target
	on_target_invalidated = {

	}

	# Scripted value to determine if the AI will select this intent or not
	# Selects the weighted random intent based on their score
	#
	# root = character picking this intent
	# scope:activity = activity they are picking for
	ai_will_do = {

	}

	# What AI targets will be considered, can be scripted multiple times to combine lists, same as in character_interaction.info
	# Already filters down if they are a participant in the activity, if they are not they are skipped and do not count against the max check
	ai_targets = {
		ai_recipients = type 	# Which characters does the ai consider as recipient for the interaction, can be scripted multiple times to combine lists
								# Available lists are in the "ai_targets" section of character_interaction.info
		max = integer 			# Maximum number of targets to consider, unset considers all of them, will consider random targets that it filters too
		chance = 0-1			# A low chance, such as 0.25, randomly excludes that number of characters from being checked - this is useful for saving performance
	}

	# Quick code efficient triggers to check for valid targets, same as in character_interaction.info
	ai_target_quick_trigger = {
		adult = yes 				# The target needs to be adult
		attracted_to_owner = yes	# The target needs to be attracted to owner
		owner_attracted = yes		# Owner needs to be attracted to the target
		prison = yes 				# Target must be in prison
	}

	# Scripted value to determine what valid target should be picked for the intent
	# Selects the weighted random target based on their score
	#
	# root = character picking this intent
	# scope:target = character that is the target
	# scope:special_option = the selected special option of the activity (if present)
	ai_target_score = {

	}

	icon = "file_name" # Will default to object key if not specified to override

	scripted_animation = "animation_key"
	
	# root = character who has this intent
	scripted_animation = {
		<inline scripted animation>
	}
}

Localization:
key: "Name of intent" # CHARACTER and TARGET_CHARACTER
key_desc: "Description of the intent" # CHARACTER and TARGET_CHARACTER
