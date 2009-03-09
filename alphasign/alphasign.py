#!/usr/bin/python
import datetime
import os
import sys
import serial

import constants


class Alpha:
  def __init__(self, device="/dev/ttyS0"):
    self.device   = device
    self.type     = "Z"            # Type Code (see protocol)
    self.address  = "00"           # Sign Address (see protocol)
    self.mode     = "rotate"       # Default display mode
    self.position = "middle_line"  # Appropriate for one-line signs
    self.debug    = False

  def connect(self):
    """Establish connection to the device.

    Args:
      device: character device (default: /dev/ttyS0)
    """
    # TODO(ms): these settings can probably be tweaked and still support most of
    # the devices.
    self._conn = serial.Serial(port=self.device,
                               baudrate=4800,
                               parity=serial.PARITY_EVEN,
                               stopbits=serial.STOPBITS_TWO,
                               timeout=1,
                               xonxoff=0,
                               rtscts=0)

  def disconnect(self):
    if self._conn:
      self._conn.close()

  def _packet(self, contents):
    pkt = ("%s%s%s%s%s%s%s" % (constants.NUL * 5, constants.SOH, self.type,
                               self.address, constants.STX, contents,
                               constants.EOT))
    return pkt

  def _write(self, packet):
    if not self._conn:
      return
    if self.debug:
      print "Writing packet: %s" % repr(packet)
    self._conn.write(packet)

  def write_text(self, msg, label="A"):
    # [WRITE_TEXT][File Label][ESC][Display Position][Mode Code]
    #   [Special Specifier][ASCII Message]
    packet = self._packet("%s%s%s%s%s%s" % (constants.WRITE_TEXT, label,
                                            constants.ESC,
                                            constants.positions[self.position],
                                            constants.modes[self.mode],
                                            msg))
    self._write(packet)

  def create_string(self, string_label="1", string_size=32):
    """Create a STRING.

    This is necessary to allocate memory for the STRING on the sign

    Args:
      string_label: label of the STRING to create
      string_size: size of the STRING to create, in bytes. 125 max.
                   Default is 32.
    """
    if string_size > 125:
      string_size = 125
    size_hex = "%04x" % string_size
    packet = self._packet("%s%s%s%s%s%s%s%s%s%s%s%s%s" %
                          (constants.WRITE_SPECIAL, "\$",
                           "A",          # call label.. why does this matter?
                           "A",          # text file type
                           "U",          # this TEXT file is unlocked
                           "0100",       # text file size in hex
                           "FF",         # text file's start time (FF = always)
                           "00",         # text file's stop time
                           string_label,
                           "B",          # string file type
                           "L",          # this string file is locked
                           size_hex,
                           "0000"))      # padding
    self._write(packet)

  def write_string(self, data, label="1"):
    """Write a STRING.

    Args:
      data: data to write
      label: STRING label to write
    """
    packet = self._packet("%s%s%s" % (constants.WRITE_STRING, label, data))
    self._write(packet)

  def call_string(self, string_label="1"):
    """Call a STRING.

    This is for inserting a STRING file into a TEXT file.

    Args:
      string_label: label of string to call (default: 1)

    Returns:
      control code of specified string label
    """
    return "\x10%s" % string_label

  def call_date(self, format=0):
    """Call date for insertion into a TEXT file.

    Args:
      format: integer from 0 to 9
                0 - MM/DD/YY
                1 - DD/MM/YY
                2 - MM-DD-YY
                3 - DD-MM-YY
                4 - MM.DD.YY
                5 - DD.MM.YY
                6 - MM DD YY
                7 - DD MM YY
                8 - MMM.DD, YYYY
                9 - Day of week

    Returns:
      formatted string to use in a TEXT
    """
    if format < 0 or format > 9:
      format = 0
    return "\x0B%s" % format

  def call_time(self):
    """Call time for insertion into a TEXT file.

    Returns:
      formatted string to use in a TEXT
    """
    return "\x13"

  def set_mode(self, mode):
    """FIXME
    """
    if mode in self.modes:
      self.mode = mode
    # FIXME: error handling for invalid mode

  def set_position(self, mode):
    """FIXME
    """
    if position in self.positions:
      self.position = position
    # FIXME: error handling

  def clear_memory(self):
    """Clear the sign's memory.
    """
    packet = self._packet("%s%s" % (constants.WRITE_SPECIAL, "$"))
    self._write(packet)

  def beep(self, frequency=0, duration=0.1, repeat=0):
    """Make the sign beep.

    Args:
      frequency: frequency integer (not in Hz), 0 - 254
      duration: beep duration, 0.1 - 1.5
      repeat: number of times to repeat, 0 - 15
    """
    if frequency < 0:
      frequency = 0
    elif frequency > 254:
      frequency = 254

    duration = int(duration / 0.1)
    if duration < 1:
      duration = 1
    elif duration > 15:
      duration = 15

    if repeat < 0:
      repeat = 0
    elif repeat > 15:
      repeat = 15

    packet = self._packet("%s%s%02X%X%X" % (constants.WRITE_SPECIAL, "(2",
                                            frequency, duration, repeat))
    self._write(packet)

  def soft_reset(self):
    """Perform a soft reset on the sign.

    This is non-destructive and does not clear the sign's memory.
    """
    packet = self._packet("%s%s" % (constants.WRITE_SPECIAL, ","))
    self._write(packet)

  def set_day(self, day=None):
    """Set the day of the week on the sign.

    If the argument is omitted, today's day will be used.

    Args:
      day (optional): integer between 1 (Sunday) and 7 (Saturday)
    """
    if day is None or day < 1 or day > 7:
      day = datetime.datetime.today().weekday() + 1
    packet = self._packet("%s%s%s" % (constants.WRITE_SPECIAL, "&", day))
    self._write(packet)

  def set_date(self, year=None, month=None, day=None):
    """Sets the date in the memory of the sign. This must be done each day to
    keep the clock 'up to date', because the sign will not automatically advance
    the day.

    If the date is not specified in the arguments, today's date will be used.

    Args:
      year (optional): two-digit year (98, 99, 00, ...)
      month (optional): integer month (1, 2, ..., 12)
      day (optional): integer day (1, ..., 31)
    """
    today = datetime.datetime.today()
    if year is None:
      year = str(today.year)[2:4]
    if month is None:
      month = today.month
    if day is None:
      day = today.day

    packet = self._packet("%s%s%02d%02d%02d" % (constants.WRITE_SPECIAL, ";",
                                                year, month, day))
    self._write(packet)

  def set_time(self, hour=None, minute=None):
    """Sets ths hour and minute of the internal clock on the sign.

    If the time is not specified in the arguments, the time now will be used.

    Args:
      hour: hour in 24-hour format (18 instead of 6 for 6PM)
      minute: minute (0 - 59)
    """
    now = datetime.datetime.today()
    if hour is None:
      hour = now.hour
    if minute is None:
      minute = now.minute

    packet = self._packet("%s%s%02d%02d" % (constants.WRITE_SPECIAL, "\x20",
                                            hour, minute))
    self._write(packet)

  def set_time_format(self, format=1):
    """Sets the time format on the sign.

    Args:
      format: 1 - 24-hour (military) time
              0 - 12-hour (standard am/pm) format
    """
    if format < 0 or format > 1:
      format = 1
    byte = (format == 0) and "S" or "M"
    packet = this._packet("%s%s%s" % (constants.WRITE_SPECIAL, "\x27", byte))
    self._write(packet)

  def color(self, color="autocolor"):
    """Returns color code for a specified color.

    Args:
      color: color string

    Returns:
      FIXME
    """
    if color not in constants.colors:
      color = "autocolor"
    return "%s%s" % ("\x1C", constants.colors[color])

  def charset(self, charset="five_high_std"):
    """Returns control code for a specified character set.

    Args:
      charset: charset name string

    Returns:
      FIXME
    """
    if charset not in constants.charsets:
      charset = "five_high_std"
    return "%s%s" % ("\x1A", constants.charsets[charset])

  def extchar(self, extchar="left_arrow"):
    """Returns control code for a specified extended character.

    Args:
      extchar: extended character name

    Returns:
      FIXME
    """
    if extchar not in constants.extchars:
      extchar = "left_arrow"
    return "%s%s" % ("\x08", constants.extchars[extchar])

  def spacing(self, option=0):
    """Returns control code to set the character spacing.

    Args:
      option: 0 - set proportional characters
              1 - fixed width left justified characters

    Returns:
      FIXME
    """
    byte = (option == 0) and "0" or "1"
    return "\x1E%s" % byte

  def speed(self, speed):
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

