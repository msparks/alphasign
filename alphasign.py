#!/usr/bin/python
import datetime
import os
import sys
import serial


class Alpha:
  # Display Modes (p89)
  modes = {
    "rotate":             "a",
    "hold":               "b",
    "flash":              "c",
    "roll_up":            "e",
    "roll_down":          "f",
    "roll_left":          "g",
    "roll_right":         "h",
    "wipe_up":            "i",
    "wipe_down":          "j",
    "wipe_left":          "k",
    "wipe_right":         "l",
    "scroll":             "m",
    "automode":           "o",
    "roll_in":            "p",
    "roll_out":           "q",
    "wipe_in":            "r",
    "wipe_out":           "s",
    "compressed_rotate":  "t",  # only available on certain sign models
    "explode":            "u",  # alpha 3.0 protocol
    "clock":              "v",  # alpha 3.0 protocol
    # Special Modes
    "twinkle":            "n0",
    "sparkle":            "n1",
    "snow":               "n2",
    "interlock":          "n3",
    "switch":             "n4",
    "slide":              "n5",  # only Betabrite 1036 (same as CYCLE_COLORS?)
    "spray":              "n6",
    "starburst":          "n7",
    "welcome":            "n8",
    "slot_machine":       "n9",
    "news_flash":         "nA",  # only Betabrite 1036
    "trumpet_animation":  "nb",  # only betabrite 1036
    "cycle_colors":       "nC",  # only AlphaEclipse 3600
    # Special Graphics (these display before the message)
    "thank_you":          "nS",
    "no_smoking":         "nU",
    "dont_drive_drive":   "nV",
    "running_animal":     "nW",
    "fish_animation":     "nW",
    "fireworks":          "nX",
    "turbo_car":          "nY",
    "balloon_animation":  "nY",
    "cherry_bomb":        "nZ",
  }

  # Display Positions
  positions = {
    "middle_line":        "\x20",
    "top_line":           "\x22",
    "bottom_line":        "\x26",
    "fill":               "\x30",
    "left":               "\x31",
    "right":              "\x32",
  }

  # Character Sets
  charsets = {
    "five_high_std":      "1",
    "five_stroke":        "2",
    "seven_high_std":     "3",
    "seven_stroke":       "4",
    "seven_high_fancy":   "5",
    "ten_high_std":       "6",
    "seven_shadow":       "7",
    "full_height_fancy":  "8",
    "full_height_std":    "9",
    "seven_shadow_fancy": ":",
    "five_wide":          ";",
    "seven_wide":         "<",
    "seven_fancy_wide":   "=",
    "wide_stroke_five":   ">",
    # The following four only work on Alpha 2.0 and Alpha 3.0 protocols
    "five_high_cust":     "W",
    "seven_high_cust":    "X",
    "ten_high_cust":      "Y",
    "fifteen_high_cust":  "Z",
  }

  # Extended characters
  extchars = {
    "up_arrow":           "\x64",
    "down_arrow":         "\x65",
    "left_arrow":         "\x66",
    "right_arrow":        "\x67",
    "pacman":             "\x68",
    "sail_boat":          "\x69",
    "ball":               "\x6A",
    "telephone":          "\x6B",
    "heart":              "\x6C",
    "car":                "\x6D",
    "handicap":           "\x6E",
    "rhino":              "\x6F",
    "mug":                "\x70",
    "satellite_dish":     "\x71",
    "copyright_symbol":   "\x72",
    "male_symbol":        "\x73",
    "female_symbol":      "\x74",
    "bottle":             "\x75",
    "diskette":           "\x76",
    "printer":            "\x77",
    "musical_note":       "\x78",
    "infinity_symbol":    "\x79",
  }

  # Counters
  # We have 5 of them.
  counters = {
    1:                    "z",
    2:                    "{",
    3:                    "|",
    4:                    "}",
    5:                    "-",
  }

  # Colors
  colors = {
    "red":                "1",
    "green":              "2",
    "amber":              "3",
    "dim_red":            "4",
    "dim_green":          "5",
    "brown":              "6",
    "orange":             "7",
    "yellow":             "8",
    "rainbow_1":          "9",
    "rainbow_2":          "A",
    "color_mix":          "B",
    "autocolor":          "C",
  }

  # Command Codes
  WRITE_TEXT            = "A"  # Write TEXT file (p18)
  READ_TEXT             = "B"  # Read TEXT file (p19)
  WRITE_SPECIAL         = "E"  # Write SPECIAL FUNCTION commands (p21)
  READ_SPECIAL          = "F"  # Read SPECIAL FUNCTION commands (p29)
  WRITE_STRING          = "G"  # Write STRING (p37)
  READ_STRING           = "H"  # Read STRING (p38)
  WRITE_SMALL_DOTS      = "I"  # Write SMALL DOTS PICTURE file (p39)
  READ_SMALL_DOTS       = "J"  # Read SMALL DOTS PICTURE file (p41)
  WRITE_RGB_DOTS        = "K"  # Write RGB DOTS PICTURE file (p44)
  READ_RGB_DOTS         = "L"  # Read RGB DOTS PICTURE file (p46)
  WRITE_LARGE_DOTS      = "M"  # Write LARGE DOTS PICTURE file (p42)
  READ_LARGE_DOTS       = "N"  # Read LARGE DOTS PICTURE file (p43)
  WRITE_ALPHAVISION     = "O"  # Write ALPHAVISION BULLETIN (p48)
  SET_TIMEOUT           = "T"  # Set Timeout Message (p118) (Alpha 2.0/3.0)

  # Constants used in transmission packets
  NUL                   = "\x00"  # NULL
  SOH                   = "\x01"  # Start of Header
  STX                   = "\x02"  # Start of TeXt (precedes a command code)
  ETX                   = "\x03"  # End of TeXt
  EOT                   = "\x04"  # End Of Transmission
  #ENQ                   = "\x05"  # Enquiry
  #ACK                   = "\x06"  # Acknowledge
  BEL                   = "\x07"  # Bell
  BS                    = "\x08"  # Backspace
  HT                    = "\x09"  # Horizontal tab
  LF                    = "\x0A"  # Line Feed
  NL                    = "\x0A"  # New Line
  VT                    = "\x0B"  # Vertical Tab
  #FF                    = "\x0C"  # Form Feed
  #NP                    = "\x0C"  # New Page
  CR                    = "\x0D"  # Carriage Return
  CAN                   = "\x18"  # Cancel
  SUB                   = "\x1A"  # Substitute (select charset)
  ESC                   = "\x1B"  # Escape character


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
    pkt = ("%s%s%s%s%s%s%s" % (self.NUL * 5, self.SOH, self.type, self.address,
                               self.STX, contents, self.EOT))
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
    packet = self._packet("%s%s%s%s%s%s" % (self.WRITE_TEXT, label, self.ESC,
                                            self.positions[self.position],
                                            self.modes[self.mode],
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
                          (self.WRITE_SPECIAL, "\$",
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
    packet = self._packet("%s%s%s" % (self.WRITE_STRING, label, data))
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
    packet = self._packet("%s%s" % (self.WRITE_SPECIAL, "$"))
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

    packet = self._packet("%s%s%02X%X%X" % (self.WRITE_SPECIAL, "(2",
                                            frequency, duration, repeat))
    self._write(packet)

  def soft_reset(self):
    """Perform a soft reset on the sign.

    This is non-destructive and does not clear the sign's memory.
    """
    packet = self._packet("%s%s" % (self.WRITE_SPECIAL, ","))
    self._write(packet)

  def set_day(self, day=None):
    """Set the day of the week on the sign.

    If the argument is omitted, today's day will be used.

    Args:
      day (optional): integer between 1 (Sunday) and 7 (Saturday)
    """
    if day is None or day < 1 or day > 7:
      day = datetime.datetime.today().weekday() + 1
    packet = self._packet("%s%s%s" % (self.WRITE_SPECIAL, "&", day))
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

    packet = self._packet("%s%s%02d%02d%02d" % (self.WRITE_SPECIAL, ";",
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

    packet = self._packet("%s%s%02d%02d" % (self.WRITE_SPECIAL, "\x20",
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
    packet = this._packet("%s%s%s" % (self.WRITE_SPECIAL, "\x27", byte))
    self._write(packet)

  def color(self, color="autocolor"):
    """Returns color code for a specified color.

    Args:
      color: color string

    Returns:
      FIXME
    """
    if color not in self.colors:
      color = "autocolor"
    return "%s%s" % ("\x1C", self.colors[color])

  def charset(self, charset="five_high_std"):
    """Returns control code for a specified character set.

    Args:
      charset: charset name string

    Returns:
      FIXME
    """
    if charset not in self.charsets:
      charset = "five_high_std"
    return "%s%s" % ("\x1A", self.charsets[charset])

  def extchar(self, extchar="left_arrow"):
    """Returns control code for a specified extended character.

    Args:
      extchar: extended character name

    Returns:
      FIXME
    """
    if extchar not in self.extchars:
      extchar = "left_arrow"
    return "%s%s" % ("\x08", self.extchars[extchar])

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


def main():
  sign = Alpha("/dev/rfcomm0")
  sign.debug = True
  sign.connect()

  sign.clear_memory()
  sign.soft_reset()

  sign.disconnect()


if __name__ == "__main__":
  main()
