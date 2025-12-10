##############################################################
# Structure 
#
# War Stances are description of AI behavior during a war. They are selected 
#	based on the AI's relative power (army size taking elite troops into account) to the 
#	involved parties, and the side of this AI (attacker or defender).
# The coordinator will assume the best scoring stance and prioritize its target
#	following a list. The final outcome would be a scoring system for provinces to move
#	armies to (follow enemy armies, siege wargoal provinces), or to camp in (defend my capital).
#
# Please remember to keep all priorities between 1 and 1000 and to avoid area overlaps.
##############################################################

war_stance = {

	### Brief: side ( enum )
	# Which side does this war stance work for? Must be set. 
	#
	# Enums: 
	#	attacker
	# 	defender
	#
	side = none

	### Brief: behaviour_attributes ( enum bitmask container )
	# Under what circumstances will we evaluate this particular stance?
	# This happens before we evaluate can_be_picked. At least one of 
	# these must be set to yes.
	#
	behaviour_attributes = {

		### Brief: stronger ( bool )
		# This is applied when the side is stronger than the other side
		#
		# Defaults to no, meaning it is not checked. 
		#
		stronger = yes

		### Brief: weaker ( bool )
		# This is applied when the side is weaker than the other side
		#
		# Defaults to no, meaning it is not checked. 
		#
		weaker = yes

		### Brief: desperate ( bool )
		# This is applied when the side is significantly weaker AND is
		# about to lose the war or only has one landed title left. 
		# Is only used by the defender side.
		#
		# Defaults to no, meaning it is not checked. 
		#
		desperate = yes
	}

	### Brief: can_be_picked ( trigger )
	# Checks if the war stance is valid for the war in question
	# 
	# Supported scopes:
	#		root (War)
	#			The War in question. Supports all other scopes found within
	#			a War Scope.
	#
	can_be_picked = {}

	### Brief: ai_will_do ( Fixed Point Scripted Value )
	# Scripted value to determine the weight of this war stance for the war 
	# coordinator. 
	# 
	# Supported scopes:
	#		root (War)
	#			The War in question. Supports all other scopes found within
	#			a War Scope.
	#
	ai_will_do = {}

	### Brief: enemy_unit_priority ( int32 )
	# Priority score added for an enemy unit half our strength. Falls off 
	# towards zero and our full strength
	enemy_unit_priority = x

	### Brief: objectives
	# List of objectives that the AI war coordinator will prioritize and areas
	# it will operate in. Can define multiple blocks of objectives and the 
	# coordinator will look for valid objectives from top to bottom.
	#
	# Valid objectives:
	# 		wargoal_province
	#			The war goal provinces.
	#
	# 		enemy_unit_province
	#			Provinces with enemy unit stacks (that can be seen).
	#
	# 		enemy_capital_province
	#			The capital province of the enemy.
	#
	# 		capital_province
	#			The capital province of your side.
	#
	# 		enemy_province
	#			Enemy provinces.
	#
	# 		enemy_ally_province
	#			Enemy allies' provinces.
	#
	# 		province
	#			Your own provinces.
	#
	#		defend_wargoal_province
	#			Fallback to defend the wargoal. Ignores the typical ignoring of goals that won't start a siege nor start a combat. 
	# 
	# Syntax:
	#	objective_name = priority_value (integer between 0 and 1000)
	#
	# supported only by enemy_unit_province:
	#	enemy_unit_province = { 
	#		priority = priority_value
	#		area = area_to_consider (see below)
	#	}
objectives = {

		### Brief: objective (int, priority)
		#
		# Provide a priority value between 0 and 1000
		enemy_province = 200
		
		### Brief: objective (object, area-based priority)
		#
		# Object-style objectives are only valid for enemy_unit_province.
		# You can specify multiple areas, the priority will be applied to all provinces that match the area
		enemy_unit_province = {

			### Brief: priority (int, priority)
			#
			# Provide a priority value between 0 and 1000
			priority = 250

			### Brief: area (objective area)
			#
			# can be one of:
			#	wargoal
			#	primary_attacker
			#	primary_attacker_ally
			#	primary_defender
			#	primary_defender_ally
			area = wargoal
		}
	}
}

# Notice: enemy_unit_province areas may not overlap. if you define an area objective 
#	in a block you may not use it anywhere else in the objectives definition.
#	The following script would rise an error and the second objective would not be created:
# ----------------------------------
#	enemy_unit_province = { 
#		priority = 50
#		area = wargoal
#	}
#	enemy_unit_province = { 
#		priority = 100
#		area = wargoal			# <- overlap on area = wargoal
#		area = primary_attacker
#	}	
# ----------------------------------
#
### Examples
# 	this is an aggressive but focused objective that makes the coordinator target:
#	* the wargoal provinces
#	* enemy units in the war goal area or in the defender's lands
# ----------------------------------
#	objectives = {
#		wargoal_province = 500
#		
#		enemy_unit_province = {
#			priority = 250
#			area = wargoal
#			area = primary_defender
#		}
#	}
# ----------------------------------
#
# 	this is a defensive objective that is put after the aggressive one at very low priority,
# 	so that the coordinator knows what to do in case there are no more targets in the objective above.
# ----------------------------------
#	objectives = {
#		defend_wargoal_province = 5
#	}
# ----------------------------------