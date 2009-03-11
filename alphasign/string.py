import constants
from packet import Packet


class String(object):
  def __init__(self, data=None, label=None, size=None):
    if label is None:
      label = "1"
    if size is None:
      size = 32
    if len(data) > size:
      size = len(data)
    if size > 125:
      size = 125
    if size < 1:
      size = 1
    self.label = label
    self.size = size
    self.data = data

  def allocate(self):
    """Create a STRING.

    This is necessary to allocate memory for the STRING on the sign

    Args:
      label: label of the STRING to create
      size: size of the STRING to create, in bytes. 125 max.
    """
    size_hex = "%04x" % self.size
    packet = Packet("%s%s%s%s%s%s%s%s%s%s%s%s%s" %
                    (constants.WRITE_SPECIAL, "\$",
                     "A",          # call label.. why does this matter?
                     "A",          # text file type
                     "U",          # this TEXT file is unlocked
                     "0100",       # text file size in hex
                     "FF",         # text file's start time (FF = always)
                     "00",         # text file's stop time
                     self.label,
                     "B",          # string file type
                     "L",          # this string file is locked
                     size_hex,
                     "0000"))      # padding
    return packet

  def call(self):
    """Call a STRING.

    This is for inserting a STRING file into a TEXT file.

    Returns:
      control code and specified string label
    """
    return "\x10%s" % self.label

  def __str__(self):
    return str(Packet("%s%s%s" % (constants.WRITE_STRING, self.label,
                                  self.data)))

  def __repr__(self):
    return repr(self.__str__())

