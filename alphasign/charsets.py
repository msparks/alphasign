"""
Character constants can be used to change the font style in TEXT
(:class:`alphasign.text.Text`) and STRING (:class:`alphasign.string.String`)
files.

--------------
Character sets
--------------

The following character set constants are defined:

* :const:`FIVE_HIGH_STD`
* :const:`FIVE_STROKE`
* :const:`SEVEN_HIGH_STD`
* :const:`SEVEN_STROKE`
* :const:`SEVEN_HIGH_FANCY`
* :const:`TEN_HIGH_STD`
* :const:`SEVEN_SHADOW`
* :const:`FULL_HEIGHT_FANCY`
* :const:`FULL_HEIGHT_STD`
* :const:`SEVEN_SHADOW_FANCY`
* :const:`FIVE_WIDE`
* :const:`SEVEN_WIDE`
* :const:`SEVEN_FANCY_WIDE`
* :const:`WIDE_STROKE_FIVE`

The following character sets are available only on Alpha 2.0 and 3.0 protocols:

* :const:`FIVE_HIGH_CUST`
* :const:`SEVEN_HIGH_CUST`
* :const:`TEN_HIGH_CUST`
* :const:`FIFTEEN_HIGH_CUST`

--------------------
Character attributes
--------------------

The following character attribute constants are defined:

* :const:`WIDE_ON`
* :const:`WIDE_OFF`
* :const:`DOUBLE_WIDE_ON`
* :const:`DOUBLE_WIDE_OFF`
* :const:`DOUBLE_HIGH_ON`
* :const:`DOUBLE_HIGH_OFF`
* :const:`TRUE_DESCENDERS_ON`
* :const:`TRUE_DESCENDERS_OFF`
* :const:`FIXED_WIDTH_ON`
* :const:`FIXED_WIDTH_OFF`
* :const:`FANCY_ON`
* :const:`FANCY_OFF`
* :const:`AUXILIARY_PORT_ON` -- Series 4000 & 7000 signs only.
* :const:`AUXILIARY_PORT_OFF`
* :const:`SHADOW_CHARACTERS_ON` -- Betabrite model 1036 and AlphaPriemere 9000 signs only.
* :const:`SHADOW_CHARACTERS_OFF`

-----------------
Character spacing
-----------------

The following character spacing constants are defined:

* :const:`PROPORTIONAL` -- default
* :const:`FIXED_WIDTH` -- fixed width left justified

--------
Examples
--------

Make a text file using the :const:`FIVE_WIDE` charset::

  msg = alphasign.Text("%sthis is wide" % alphasign.charsets.FIVE_WIDE,
                       label="A")

"""

# Character sets
FIVE_HIGH_STD         = "\x1A1"
FIVE_STROKE           = "\x1A2"
SEVEN_HIGH_STD        = "\x1A3"
SEVEN_STROKE          = "\x1A4"
SEVEN_HIGH_FANCY      = "\x1A5"
TEN_HIGH_STD          = "\x1A6"
SEVEN_SHADOW          = "\x1A7"
FULL_HEIGHT_FANCY     = "\x1A8"
FULL_HEIGHT_STD       = "\x1A9"
SEVEN_SHADOW_FANCY    = "\x1A:"
FIVE_WIDE             = "\x1A;"
SEVEN_WIDE            = "\x1A<"
SEVEN_FANCY_WIDE      = "\x1A="
WIDE_STROKE_FIVE      = "\x1A>"

# Alpha 2.0 and 3.0 only
FIVE_HIGH_CUST        = "\x1AW"
SEVEN_HIGH_CUST       = "\x1AX"
TEN_HIGH_CUST         = "\x1AY"
FIFTEEN_HIGH_CUST     = "\x1AZ"

# Character attributes
WIDE_ON               = "\x1D01"
WIDE_OFF              = "\x1D00"
DOUBLE_WIDE_ON        = "\x1D11"
DOUBLE_WIDE_OFF       = "\x1D10"
DOUBLE_HIGH_ON        = "\x1D21"
DOUBLE_HIGH_OFF       = "\x1D20"
TRUE_DESCENDERS_ON    = "\x1D31"
TRUE_DESCENDERS_OFF   = "\x1D30"
FIXED_WIDTH_ON        = "\x1D41"
FIXED_WIDTH_OFF       = "\x1D40"
FANCY_ON              = "\x1D51"
FANCY_OFF             = "\x1D50"
AUXILIARY_PORT_ON     = "\x1D61"
AUXILIARY_PORT_OFF    = "\x1D60"
SHADOW_CHARACTERS_ON  = "\x1D71"
SHADOW_CHARACTERS_OFF = "\x1D70"

FLASH_ON              = "\x071"
FLASH_OFF             = "\x070"

# Character spacing
PROPORTIONAL          = "\x1E0"
FIXED_WIDTH           = "\x1E1"
