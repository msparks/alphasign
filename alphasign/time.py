import constants
from packet import Packet


class Time(object):
  def call(self):
    """Call time for insertion into a TEXT file.

    Returns:
      formatted string to use in a TEXT
    """
    return "\x13"

  def set(self, hour=None, minute=None):
    """Sets ths hour and minute of the internal clock on the sign.

    If the time is not specified in the arguments, the time now will be used.

    Args:
      hour: hour in 24-hour format (18 instead of 6 for 6PM)
      minute: minute (0 - 59)

    Returns:
      Packet object
    """
    now = datetime.datetime.today()
    if hour is None:
      hour = now.hour
    if minute is None:
      minute = now.minute

    packet = Packet("%s%s%02d%02d" % (constants.WRITE_SPECIAL, "\x20",
                                      hour, minute))
    return packet

  def set_format(self, format=1):
    """Sets the time format on the sign.

    Args:
      format: 1 - 24-hour (military) time
              0 - 12-hour (standard am/pm) format

    Returns:
      Packet object
    """
    if format < 0 or format > 1:
      format = 1
    byte = (format == 0) and "S" or "M"
    packet = Packet("%s%s%s" % (constants.WRITE_SPECIAL, "\x27", byte))
    return packet