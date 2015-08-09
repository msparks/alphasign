import constants
import datetime
from packet import Packet


class Date(object):
  """Class for setting and accessing the date."""

  def call_date(self, format=0):
    """Call date for insertion into a TEXT file.

    :param format: integer from 0 to 9:
                     0 - MM/DD/YY;
                     1 - DD/MM/YY;
                     2 - MM-DD-YY;
                     3 - DD-MM-YY;
                     4 - MM.DD.YY;
                     5 - DD.MM.YY;
                     6 - MM DD YY;
                     7 - DD MM YY;
                     8 - MMM.DD, YYYY;
                     9 - Day of week

    :returns: formatted string to use in a TEXT
    :rtype: string
    """
    if format < 0 or format > 9:
      format = 0
    return "\x0B%s" % format

  def set(self, year=None, month=None, day=None):
    """Sets the date in the memory of the sign. This must be done each day to
    keep the clock 'up to date', because the sign will not automatically advance
    the day.

    If the date is not specified in the arguments, today's date will be used.

    :param year: (optional) two-digit year (98, 99, 00, ...)
    :param month: (optional) integer month (1, 2, ..., 12)
    :param day: (optional) integer day (1, ..., 31)

    :rtype: :class:`alphasign.packet.Packet` object
    """
    today = datetime.datetime.today()
    if year is None:
      year = str(today.year)[2:4]
    if month is None:
      month = today.month
    if day is None:
      day = today.day

    packet = Packet("%s%s%02d%02d%02d" % (constants.WRITE_SPECIAL, ";",
                                          month, day, int(year)))
    return packet

  def set_day(self, day=None):
    """Set the day of the week on the sign.

    If the argument is omitted, today's day will be used.

    :param day: (optional) integer between 1 (Sunday) and 7 (Saturday)

    :rtype: :class:`alphasign.packet.Packet` object
    """
    if day is None or day < 1 or day > 7:
      day = datetime.datetime.today().weekday() + 1
    packet = Packet("%s%s%s" % (constants.WRITE_SPECIAL, "&", day))
    return packet
