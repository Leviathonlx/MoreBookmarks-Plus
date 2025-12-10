Structure:

# Story cycle type
key = {
	# Effect is executed when story just has been created
	# root - active story cycle
	# scope:story - same as root
	on_setup = {}

	# Effect is executed when story is ended by end_story effect
	# root - active story cycle
	# scope:story - same as root
	on_end = {}

	# Effect is executed when story owner dies. It's a good time to set new story owner
	# root - active story cycle
	# scope:story - same as root
	on_owner_death = {}

	# Any number of effect groups can be defined for story cycle type
	effect_group = {

		# Duration between attempts to execute this effect group . Can be fixed value or picked randomly from a range
		days/weeks/months/years = <int>/{<int>..<int>}

		# Chance that effect group will fire in the interval [0..100]
		# It chance doesn't proc, another attempt will be made again on next duration tick
		# If no chance is specified, effect group is always triggered
		chance = <fixed_point>

		# Effect group will fire only if trigger is satisfied
		# root - active story cycle
		# scope:story - same as root
		trigger = {}

		# Execute effect only if trigger is valid
		# Only one independent triggered_effect can be defined
		# root - active story cycle
		# scope:story - same as root
		triggered_effect = {
			trigger = {}
			effect = {}
		}

		# Execute at most one valid triggered effect picked at random
		# Any number of triggered_effect can be put inside random_valid block
		# root - active story cycle
		# scope:story - same as root
		random_valid = {
			triggered_effect = {}
			...
			triggered_effect = {}
		}

		# Execute at most one first valid triggered effect
		# Any number of triggered_effect can be put inside first_valid block
		# root - active story cycle
		# scope:story - same as root
		first_valid = {
			triggered_effect = {}
			...
			triggered_effect = {}
		}

		# Effect is only executed if none of the triggered effect were fired before
		# root - active story cycle
		# scope:story - same as root
		fallback = {}
	}
	...
	effect_group = {}
}
