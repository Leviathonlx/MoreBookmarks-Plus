# CK3_Color_Storage
Tool for keeping/resetting landed title colors in CK3.

`CK3_Color_Storage` can be added as a submodule to your repo and then you can invoke `generate_submod_files.py` which will generate the necessary titles in the folder `CK3CS`; after running `generate_submod_files.py`, simply copy the contents of CK3CS into your mod (and remove the .gitignore files as well).

Essentially, all this code does is (for the title tiers you specify), it creates a title called `d_<TITLE_NAME>_color` that stores the titles actual color at game start and adds a title-scoped scripted effect `reset_color_effect` to reset a title's color (if the title has an associated color storage title.

Other Notes:
1). It might be necessary to rename `common/on_action/CK3CS_titles.txt` to something like `common/on_action/000_CK3CS_titles.txt` to ensure the title colors are stored prior to other game start on actions, on the off chance the code calls some title color changes before storing title colors.

2). We have to explicitly name each title because PDX's quasi-templating is literal and as such, we can't simply template `title:d_$TITLE_NAME$_color = { set_color_from_title = $TITLE_NAME$ }`, as calling TITLE_NAME = this will explicitly replaced $TITLE_NAME$ with the `this` literal string. Hence why `common/on_action/CK3CS_titles.txt` will have a literal list of every title in your mod instead of some iterations over title lists.

3). This code uses regular expressions, so it is quite possible the title list might reference some non-existent titles due to string matching. This should show up as a (small) list of errors in you `error.log` and should be simple enough to clean up manually.
