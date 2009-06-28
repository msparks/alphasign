import constants
from packet import Packet


class String(object):
  """Class representing a STRING file.

  :ivar data: string contained within object
  :ivar label: label of string object
  """

  def __init__(self, data=None, label=None, size=None):
    """
    :param data: initial string to insert into object
    :param label: file label (default: "1")
    :param size: maximum size of string data in bytes (default: 32)
    """
    if data is None:
      data = ""
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

    :returns: control code and specified string label
    :rtype: string
    """
    return "\x10%s" % self.label

  def __str__(self):
    return str(Packet("%s%s%s" % (constants.WRITE_STRING, self.label,
                                  self.data)))

  def __repr__(self):
    return repr(self.__str__())
