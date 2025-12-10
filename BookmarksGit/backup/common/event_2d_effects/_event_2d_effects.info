
reference_key = {

	### Brief: 2d_effect
	# A 2D effect that can be shown when the event pops up. This will show on 
	# top of the background theme, and if it is animated will begin after the
	# transition is done playing, if any. 
	#
	# In case that there are multiples the first one that fits the trigger 
	# will be the one selected.
	# 
	effect_2d =  {

		### Brief: trigger ( jomini trigger )
		# Receives the event scope to check if it's valid.
		trigger = { ... }	

		### Brief: reference ( string path )
		# Path to the bink video effect
		# 
		reference = "gfx/interface/animation/my/example/animation.bk2" 	

		### Brief: mask ( string path )
		# Path to video or texture mask to use in doing an alpha multiply on 
		# the fade video or image
		#
		mask = "path/to/my/video.bk2"

		### Brief: mask_type ( enum )
		# What type of resource the designated mask is.
		#
		# Defaults to texture
		#
		mask_type = texture | video

		### Brief: duration ( CFixedPoint )
		# How long will this effect play? If 0 it will be continous and not 
		# fade. 
		#
		# Must be greater than or equal to 0.
		duration = 0.0
	}

	effect_2d = { ... }
}