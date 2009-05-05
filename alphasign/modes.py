"""
This module defines available modes for use with TEXT files
(:class:`alphasign.text.Text`).

The following display modes are defined:

* :const:`ROTATE`
* :const:`HOLD`
* :const:`ROLL_UP`
* :const:`ROLL_DOWN`
* :const:`ROLL_LEFT`
* :const:`ROLL_RIGHT`
* :const:`WIPE_UP`
* :const:`WIPE_DOWN`
* :const:`WIPE_LEFT`
* :const:`WIPE_RIGHT`
* :const:`SCROLL`
* :const:`AUTOMODE`
* :const:`ROLL_IN`
* :const:`ROLL_OUT`
* :const:`WIPE_IN`
* :const:`WIPE_OUT`
* :const:`COMPRESSED_ROTATE` (works only on certain sign models)
* :const:`EXPLODE` (Alpha 3.0 protocol only)
* :const:`CLOCK` (Alpha 3.0 protocol only)

The following special modes are defined:

* :const:`TWINKLE`
* :const:`SPARKLE`
* :const:`SNOW`
* :const:`INTERLOCK`
* :const:`SWITCH`
* :const:`SLIDE` (only Betabrite 1036)
* :const:`SPRAY`
* :const:`STARBURST`
* :const:`WELCOME`
* :const:`SLOT_MACHINE`
* :const:`NEWS_FLASH` (only Betabrite 1036)
* :const:`TRUMPET_ANIMATION` (only Betabrite (1036)
* :const:`CYCLE_COLORS` (only AlphaEclipse 3600)

Special graphics are modes which display graphics before the message. The
following special graphics are defined:

* :const:`THANK_YOU`
* :const:`NO_SMOKING`
* :const:`DONT_DRINK_DRIVE`
* :const:`RUNNING_ANIMAL`
* :const:`FISH_ANIMATION`
* :const:`FIREWORKS`
* :const:`TURBO_CAR`
* :const:`BALLOON_ANIMATION`
* :const:`CHERRY_BOMB`

--------
Examples
--------

Make a text file stationary on the sign::

  msg = alphasign.Text("hello world", label="A", mode=alphasign.modes.HOLD)

To change the mode for an already created text file, do::

  msg.mode = alphasign.modes.ROLL_IN
"""

# Normal display modes
ROTATE            = "a"
HOLD              = "b"
FLASH             = "c"
ROLL_UP           = "e"
ROLL_DOWN         = "f"
ROLL_LEFT         = "g"
ROLL_RIGHT        = "h"
WIPE_UP           = "i"
WIPE_DOWN         = "j"
WIPE_LEFT         = "k"
WIPE_RIGHT        = "l"
SCROLL            = "m"
AUTOMODE          = "o"
ROLL_IN           = "p"
ROLL_OUT          = "q"
WIPE_IN           = "r"
WIPE_OUT          = "s"
COMPRESSED_ROTATE = "t"
EXPLODE           = "u"
CLOCK             = "v"

# Special modes
TWINKLE           = "n0"
SPARKLE           = "n1"
SNOW              = "n2"
INTERLOCK         = "n3"
SWITCH            = "n4"
SLIDE             = "n5"
SPRAY             = "n6"
STARBURST         = "n7"
WELCOME           = "n8"
SLOT_MACHINE      = "n9"
NEWS_FLASH        = "nA"
TRUMPET_ANIMATION = "nB"
CYCLE_COLORS      = "nC"

# Special graphics
THANK_YOU         = "nS"
NO_SMOKING        = "nU"
DONT_DRINK_DRIVE  = "nV"
RUNNING_ANIMAL    = "nW"
FISH_ANIMATION    = "nW"
FIREWORKS         = "nX"
TURBO_CAR         = "nY"
BALLOON_ANIMATION = "nY"
CHERRY_BOMB       = "nZ"
