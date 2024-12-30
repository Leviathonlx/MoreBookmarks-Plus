Hello! Here's the Keizer Harm map colouriser tool. Use this to make the de jure title structure of your custom map be coloured into nice gradients rather than random neon colours.

Version 1.1

There's two inputs: the settings file Settings.txt, and the titles file Titles.txt, in which you should paste the titles you wish to recolour.

### Logic ###
When you run the tool, the titles file is parsed and all the titles included are collected into the program memory. Then most of the titles are selected to be assigned new colours. Two categories of titles are skipped: top-level titles, and titles which you specify should be skipped using the following key word "#KEEPTHISCOLOUR". Put that behind the colour entry in the title definition, like here:

k_anahuac = {
	color = { 43 255 230 } #KEEPTHISCOLOUR
	...
}

The titles that need be recoloured are organised under their parent (liege) title, by tier. The highest titles (that need recolouring) should be maximally distinct from each other, the lowest titles should be subtly different shades (but still perceptibly different). The standard settings reflect that.

For example, a title structure for the tool to parse could look like this:

e_cemanahuac (green)
├k_anahuac (red)
│├d_texcoco (pink)
││├c_tenochtitlan (bright blue)
││└c_iztapalapa (violet)
│└d_xaltocan (vermillion)
│ ├c_xaltocan (maroon)
│ └c_otompan (cyan)
└k_tlaxcala (red)
 ├d_tepeticpac (navy blue)
 │├c_tepeticpac (off-white)
 │└c_tizatlan (beige)
 └d_ocotelolco (carnation)
   ├c_ocotelolco (chestnut)
   └c_quiahuiztlan (sky blue)

The empire has a defined colour, green. The others also have colours but those will be ignored by the tool. After running, the titles will look like this:

e_cemanahuac (green)
├k_anahuac (lime)
│├d_texcoco (french lime)
││├c_tenochtitlan (french lime but slightly darker)
││└c_iztapalapa (french lime but slightly yellower)
│└d_xaltocan (electric lime)
│ ├c_xaltocan (electric/lemon lime)
│ └c_otompan (electric lime but slightly whiter)
└k_tlaxcala (teal)
 ├d_tepeticpac (british racing green)
 │├c_tepeticpac (brunshwick green)
 │└c_tizatlan (british racing green but slightly bluer)
 └d_ocotelolco (dark spring green)
   ├c_ocotelolco (medium-dark spring green)
   └c_quiahuiztlan (regular spring green)

So every vassal title will be a shade of the liege title, and the higher the tier, the more drastically different it can be. You can change the settings to determine just how great the colours differences should be at each level.

Now, but what if you want to force the Tlaxcala kingdom to remain red? Fine, enter this title structure instead:
e_cemanahuac (green)
├k_anahuac (red)
│├d_texcoco (pink)
││├c_tenochtitlan (bright blue)
││└c_iztapalapa (violet)
│└d_xaltocan (vermillion)
│ ├c_xaltocan (maroon)
│ └c_otompan (cyan)
└k_tlaxcala (red) #KEEPTHISCOLOUR
 ├d_tepeticpac (navy blue)
 │├c_tepeticpac (off-white)
 │└c_tizatlan (beige)
 └d_ocotelolco (carnation)
   ├c_ocotelolco (chestnut)
   └c_quiahuiztlan (sky blue)

And you will get:

e_cemanahuac (green)
├k_anahuac (lime)
│├d_texcoco (french lime)
││├c_tenochtitlan (french lime but slightly darker)
││└c_iztapalapa (french lime but slightly yellower)
│└d_xaltocan (electric lime)
│ ├c_xaltocan (electric/lemon lime)
│ └c_otompan (electric lime but slightly whiter)
└k_tlaxcala (red)
 ├d_tepeticpac (maroon)
 │├c_tepeticpac (dark maroon)
 │└c_tizatlan (bright maroon)
 └d_ocotelolco (hot pink)
   ├c_ocotelolco (light hot pink)
   └c_quiahuiztlan (carnation pink)

The concept should be clear. Because the top-level colour is never adjusted, you can enter your entire 00_landed_titles.txt file without an issue. Some unlanded titles may be defined outside the structure, like k_papal_state in vanilla, but because they are at the root level their colours are never altered. On the other side, the tool is just fine with the input of a single empire structure, or even a single kingdom or duchy; it will similarly keep the root title(s) the same colour as before, and recolour the others in accordance with their rank (as determined by the e_, k_, etc. prefix).

New colours are generated using random values in the CIE L*a*b* 1976 colour space, which claims to be perceptually uniform. Colour difference is determined with the CIE Delta-E 2000 formula.

### Output ###

The output is the same landed titles file, but with the colours replaced with the generated ones. You can decide where the output will be generated; see Settings.txt for that.


I hope all is clear! If you have any issues, questions or suggestions, feel free to ask me on the forum thread: https://forum.paradoxplaza.com/forum/threads/tool-map-title-colouriser-automatically-generate-nice-de-jure-title-gradients-for-custom-maps.1460776/