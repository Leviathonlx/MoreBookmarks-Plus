# A relation between two houses.

example_relation_type = {
	# The level considered the "middle" of the relation.
	# This is the default level is nothing else is specified in the creation effect.
	# It's also what the relation would gravitate towards when left unaffected.
	neutral_level = <level key>

	# Relationship levels
	# (there must be at least one)
	levels =  {
		<level key> = {
			# Members of one house will have this applied to their opinion
			# of members of the other house.
			opinion = <int>

			## Cohesion contribution per month
			#
			# If this house is in a bloc (house based  confederation) , then this is how much this House Relation level
			# contributes to the total monthly cohesion change for one member house.
			#
			# For this to take effect both houses must be in the bloc.
			# This is counted for every house in the block on it's relation to another house that is also in the bloc.
			# Note that it is used twice. This is because we compute the total amount per house, and show that to the player.
			# The same relation will contribute to both House As relation to House B, and to House Bs relation to House A.
			#
			# It's the value that is provided as 'scope:base_value' in the cohesion_contribution scripted variable
			# on the confederation type. Just forwarding this will provide the default behaviour.
			#
			# The value is then finally multiplied by either COHESION_FROM_LEADER_HOUSE_RELATION_MULT or
			# COHESION_FROM_MEMBER_HOUSE_RELATION_MULT depending on if the relation involved relation the leading house, or not.
			#
			cohesion_contribution = <int>

			# Various properties of the level that can be queried from script.
			parameters = {
				<list of parameters>
			}

			## Cohesion contribution per month
			#
			# If this house is in a bloc (house based  confederation) , then this is how much this House Relation level 
			# contributes to the total monthly cohesion change for one member house.
			#
			# For this to take effect both houses must be in the bloc.
			# This is counted for every house in the block on it's relation to another house that is also in the bloc.
			# Note that it is used twice. This is because we compute the total amount per house, and show that to the player.
			# The same relation will contribute to both House As relation to House B, and to House Bs relation to House A.   
			#
			# It's the value that is provided as 'scope:base_value' in the cohesion_contribution scripted variable
			# on the confederation type. 
			# Just forwarding this will provide the default behaviour. 
			# 
			cohesion_contribution <int>
		}

		# ...
	}
}
