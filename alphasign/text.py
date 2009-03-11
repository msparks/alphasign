import constants
from packet import Packet


# Colors
RED       = "\x1C1"
GREEN     = "\x1C2"
AMBER     = "\x1C3"
DIM_RED   = "\x1C4"
DIM_GREEN = "\x1C5"
BROWN     = "\x1C6"
ORANGE    = "\x1C7"
YELLOW    = "\x1C8"
RAINBOW_1 = "\x1C9"
RAINBOW_2 = "\x1CA"
COLOR_MIX = "\x1CB"
AUTOCOLOR = "\x1CC"
# TODO(ms): need support for RGB colors

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

# Extended characters
UP_ARROW         = "\x08\x64"
DOWN_ARROW       = "\x08\x65"
LEFT_ARROW       = "\x08\x66"
RIGHT_ARROW      = "\x08\x67"
PACMAN           = "\x08\x68"
SAIL_BOAT        = "\x08\x69"
BALL             = "\x08\x6A"
TELEPHONE        = "\x08\x6B"
HEART            = "\x08\x6C"
CAR              = "\x08\x6D"
HANDICAP         = "\x08\x6E"
RHINO            = "\x08\x6F"
MUG              = "\x08\x70"
SATELLITE_DISH   = "\x08\x71"
COPYRIGHT_SYMBOL = "\x08\x72"
MALE_SYMBOL      = "\x08\x73"
FEMALE_SYMBOL    = "\x08\x74"
BOTTLE           = "\x08\x75"
DISKETTE         = "\x08\x76"
PRINTER          = "\x08\x77"
MUSICAL_NOTE     = "\x08\x78"
INFINITY_SYMBOL  = "\x08\x79"

# Display speeds
SPEED_1 = "\x15"
SPEED_2 = "\x16"
SPEED_3 = "\x17"
SPEED_4 = "\x18"
SPEED_5 = "\x19"


class Text(object):
  def __init__(self, msg=None, label=None, position=None, mode=None):
    if label is None:
      label = "A"
    self.label = label
    self.msg = msg
    # TODO(ms): need support for position and mode

  def __str__(self):
    # [WRITE_TEXT][File Label][ESC][Display Position][Mode Code]
    #   [Special Specifier][ASCII Message]
    packet = Packet("%s%s%s%s%s%s" % (constants.WRITE_TEXT, self.label,
                                      constants.ESC,
                                      constants.positions["middle_line"],
                                      constants.modes["rotate"],
                                      self.msg))
    return str(packet)

  def __repr__(self):
    return repr(self.__str__())
