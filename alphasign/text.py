import constants
from packet import Packet


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


def color(color="autocolor"):
  """Returns color code for a specified color.

  Args:
    color: color string

  Returns:
    FIXME
  """
  if color not in constants.colors:
    color = "autocolor"
  return "%s%s" % ("\x1C", constants.colors[color])


def charset(charset="five_high_std"):
  """Returns control code for a specified character set.

  Args:
    charset: charset name string

  Returns:
    FIXME
  """
  if charset not in constants.charsets:
    charset = "five_high_std"
  return "%s%s" % ("\x1A", constants.charsets[charset])


def extchar(extchar="left_arrow"):
  """Returns control code for a specified extended character.

  Args:
    extchar: extended character name

  Returns:
    FIXME
  """
  if extchar not in constants.extchars:
    extchar = "left_arrow"
  return "%s%s" % ("\x08", constants.extchars[extchar])


def spacing(option=0):
  """Returns control code to set the character spacing.

  Args:
    option: 0 - set proportional characters
            1 - fixed width left justified characters

  Returns:
    FIXME
  """
  byte = (option == 0) and "0" or "1"
  return "\x1E%s" % byte


def speed(speed):
  """Set the speed of the scrolling text.

  Args:
    speed: integer 1 (slowest) through 5 (fastest) inclusive

  Returns:
    FIXME
  """
  if speed < 1:
    speed = 1
  elif speed > 5:
    speed = 5

  n = 20 + speed
  return chr(n)
