######################################################
############## BLACKMAIL INTERACTION ################
######################################################

window = {
	name = "blackmail_interaction_window"
	datacontext = "[BlackmailInteractionWindow.GetCharacterInteractionConfirmationWindow]"
	parentanchor = center
	layer = middle

	using = Window_Background
	using = Window_Decoration_Spike

	state = {
		name = _show
		using = Animation_FadeIn_Quick
		using = Sound_WindowShow_Standard
	}

	state = {
		name = _hide
		using = Animation_FadeOut_Quick
		using = Sound_WindowHide_Standard
	}

	vbox = {
		using = Window_Margins
		set_parent_size_to_minimum = yes

		header_pattern_interaction = {
			layoutpolicy_horizontal = expanding

			blockoverride "header_text" {
				text = "[SelectLocalization( BlackmailInteractionWindow.IsBlackmail, 'blackmail_interaction', 'INTRIGUE_WINDOW_EXPOSE_TITLE' )]"
			}

			blockoverride "button_close"
			{
				onclick = "[BlackmailInteractionWindow.Close]"
			}

			icon_character_interaction = {}
		}

		### Portrait / Info

		hbox = {
			name = "portrait_and_info"
			datacontext = "[CharacterInteractionConfirmationWindow.GetRecipient]"
			layoutpolicy_horizontal = expanding
			margin = { 10 5 }

			background = {
				using = Background_Area
			}

			text_multi = {
				name = "info_text"
				multiline = yes
				autoresize = yes
				max_width = 250
				text = "[BlackmailInteractionWindow.GetDescription]"
				align = center
				#using = Font_Size_Medium
			}

			portrait_head = {
				visible = "[Character.IsValid]"

				blockoverride "portrait_transformation"
				{
					portrait_scale = { -1 1 }
					portrait_offset = { 1 0 }
				}
			}
		}

		### List
		scrollbox = {
			name = "secrets_list"
			layoutpolicy_horizontal = expanding
			layoutpolicy_vertical = expanding

			blockoverride "scrollbox_empty"
			{
				text = "BLACKMAIL_NO_SECRETS"
				visible = "[Not(BlackmailInteractionWindow.HasSecrets)]"
			}

			blockoverride "scrollbox_content"
			{
				vbox = {
					datamodel = "[BlackmailInteractionWindow.GetSecretItems]"
					layoutpolicy_horizontal = expanding
					spacing = 3

					item = {
						hbox = {
							layoutpolicy_horizontal = expanding
							spacing = 8
							button_standard = {
								layoutpolicy_horizontal = expanding
								tooltip = "[BlackmailSecretItem.GetTooltip]"
								onclick = "[BlackmailSecretItem.OnClick]"
								down = "[BlackmailSecretItem.IsSelected]"
								enabled = "[BlackmailSecretItem.IsEnabled]"
								text = "[BlackmailSecretItem.GetSecret.GetName]"

								icon = {
									size = { 26 26 }
									parentanchor = vcenter
									position = { 5 0 }
									texture = "[BlackmailSecretItem.GetSecret.GetType.GetIcon]"
								}
							}

							icon = {
								size = { 26 26 }
								texture = "gfx/interface/icons/portraits/hook_secret.dds"
								framesize = { 40 40 }
								frame = 1
								visible = "[And( BlackmailInteractionWindow.IsBlackmail, BlackmailSecretItem.IsWeakHook )]"

								datacontext = "[CharacterInteractionConfirmationWindow.GetRecipient]"
								tooltip = "INTRIGUE_WINDOW_BLACKMAIL_WEAK_HOOK_TT"
							}

							icon = {
								size = { 26 26 }
								texture = "gfx/interface/icons/portraits/hook_secret.dds"
								framesize = { 40 40 }
								frame = 2
								visible = "[And( BlackmailInteractionWindow.IsBlackmail, BlackmailSecretItem.IsStrongHook )]"

								datacontext = "[CharacterInteractionConfirmationWindow.GetRecipient]"
								tooltip = "INTRIGUE_WINDOW_BLACKMAIL_STRONG_HOOK_TT"
							}
						}
					}
				}
			}
		}

		vbox = {
			layoutpolicy_horizontal = expanding
			margin = { 0 10 }
			margin_bottom = 15
			spacing = 10

			vbox_character_interaction_effects = {
				datacontext = "[CharacterInteractionConfirmationWindow.GetEffectsDescription]"
				visible = "[BlackmailInteractionWindow.IsBlackmail]"
			}

			hbox_character_interaction_acceptance = {
				visible = "[And( BlackmailInteractionWindow.IsBlackmail, CharacterInteractionConfirmationWindow.ShouldShowAnswer )]"
				layoutpolicy_horizontal = expanding
			}

			text_multi_on_decline_summary = {
				visible = "[BlackmailInteractionWindow.IsBlackmail]"
			}

			### Send Button
			button_primary = {
				name = "send_offer_button"
				size = { 400 42 }
				enabled = "[BlackmailInteractionWindow.CanSendOffer]"
				onclick = "[BlackmailInteractionWindow.Send]"

				text = "[SelectLocalization( BlackmailInteractionWindow.IsBlackmail, CharacterInteractionConfirmationWindow.GetSendName, 'INTRIGUE_WINDOW_SECRET_EXPOSE' )]"
				using = Font_Size_Medium

				tooltip = "[BlackmailInteractionWindow.GetSendOfferTooltip]"
			}
		}
	}
}