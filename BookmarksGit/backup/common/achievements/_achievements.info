##############################################################
# Structure 
##############################################################
#
# These files comprise the Achievement Database.
#
#	Achievements Flags
#
# When we add flags etc for achievements, we need to do it in a certain roundabout way, or else it'll trigger errors
#	when running some of our automated tests. For context, these tests run the game without graphics, which for one
#	reason or another, don't read achievements.
# Thus if the only place an achievement flag/variable is read is inside the achievement script, we end up with errors
#	like these during the test:
#
# [15:36:43][jomini_effect.cpp:324]: Character flag 'rd_character_blocked_far_from_home_achievement' is set but is never used
# [15:36:43][jomini_effect.cpp:324]: Variable 'first_of_the_crusader_kings_achievement_flag' is set but is never used
# 
# Instead use the scripted achievement effects such as add_achievement_flag_effect.
# They will suppress the above errors by adding dummy usages as well.
#
# Look for all effects in achievement_effects.txt, the different effects are used for different kinds of achievement checks.

# Key of the achievement. Name and description loc keys will use this as base in achievements_l_LANGUAGE.yml
#	name:           ACHIEVEMENT_your_achievement_key
#	description:    ACHIEVEMENT_DESC_your_achievement_key
your_achievement_key = {

	### possible (trigger, optional)
	#
	# A player-character-scoped trigger that determines whether the achievement can ever be unlocked in this run.
	# This allows the player to see which achievement they can aim for in this run. Can be empty and check for variables
	#
	# Scopes:
	#	root = the character being played
	possible = {
	}

	### happened (trigger)
	#
	# A player-character-scoped trigger that determines whether the achievement was unlocked.
	# In practice we always use a custom_description trigger to be able to show custom trigger text.
	#	The custom trigger descriptions are defined in XX_track_achievement_triggers.txt in the common/trigger_localization folder.
	# After the text you can write the actual condition to unlock the achievement.
	happened = {
		custom_description = {
			# Name of the custom trigger localization. Usually the structure to use in the achievement_triggers file goes like this:
			#
			#	your_achievement_key_trigger = {
			#		global = ACHIEVEMENT_DESC_your_achievement_key
			#	}
			text = your_achievement_key_trigger

			### subject (optional)
			# scope object of the subject of the text's phrase, to be used when localizing the text's variable entities (he/she/I...).
			# This only affects the text localization. Generally unused for achievements.
			subject = {}

			### object (optional)
			# scope object of the object of the text's phrase, to be used when localizing the text's variable entities (he/she/I...).
			# This only affects the text localization. Generally unused for achievements.
			object = {}

			### value (optional)
			# scope object of a numeric value to be used in the text's phrase.
			# This only affects the text localization. Generally unused for achievements.
			value = {}

			# Everything else in this custom_description is counted as a Character-scoped trigger that checks if the current situation can unlock this achievement.
			# 
			# Scopes:
			#	root = the character being played
			exists = root.capital_province
		}
	}
}
