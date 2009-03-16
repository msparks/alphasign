"""
Character sets can be used to change the font style in TEXT and STRING files.

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
"""

# Character sets
FIVE_HIGH_STD      = "\x1A1"
FIVE_STROKE        = "\x1A2"
SEVEN_HIGH_STD     = "\x1A3"
SEVEN_STROKE       = "\x1A4"
SEVEN_HIGH_FANCY   = "\x1A5"
TEN_HIGH_STD       = "\x1A6"
SEVEN_SHADOW       = "\x1A7"
FULL_HEIGHT_FANCY  = "\x1A8"
FULL_HEIGHT_STD    = "\x1A9"
SEVEN_SHADOW_FANCY = "\x1A:"
FIVE_WIDE          = "\x1A;"
SEVEN_WIDE         = "\x1A<"
SEVEN_FANCY_WIDE   = "\x1A="
WIDE_STROKE_FIVE   = "\x1A>"

# Alpha 2.0 and 3.0 only
FIVE_HIGH_CUST     = "\x1AW"
SEVEN_HIGH_CUST    = "\x1AX"
TEN_HIGH_CUST      = "\x1AY"
FIFTEEN_HIGH_CUST  = "\x1AZ"
