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

