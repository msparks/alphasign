import constants
import modes
import positions
from packet import Packet


class Text(object):
  """Class representing a TEXT file."""
  def __init__(self, data=None, label=None, size=None,
               position=None, mode=None):
    """
    :param data: initial string to insert into object
    :param label: file label: (default: "A")
    :param size: amount of bytes to allocate for object on sign (default: 64)
    :param position: constant from :mod:`alphasign.positions`
    :param mode: constant from :mod:`alphasign.modes`
    """
    if data is None:
      data = ""
    if label is None:
      label = "A"
    if size is None:
      size = 64
    if len(data) > size:
      size = len(data)
    if size > 125:
      size = 125
    if size < 1:
      size = 1
    if position is None:
      position = positions.MIDDLE_LINE
    if mode is None:
      mode = modes.ROTATE

    self.label = label
    self.size = size
    self.data = data
    self.position = position
    self.mode = mode

  def __str__(self):
    # [WRITE_TEXT][File Label][ESC][Display Position][Mode Code]
    #   [Special Specifier][ASCII Message]
    packet = Packet("%s%s%s%s%s%s" % (constants.WRITE_TEXT, self.label,
                                      constants.ESC,
                                      self.position,
                                      self.mode,
                                      self.data))
    return str(packet)

  def __repr__(self):
    return repr(self.__str__())
