import time
import re
from itertools import imap

from alphasign import constants
from alphasign import packet

import alphasign.string
import alphasign.text


class BaseInterface(object):
  """Base interface from which all other interfaces inherit.

  This class contains utility methods for fundamental sign features.
  """

  #TODO: perhaps raise a NotImplementedError here?
  def write(self, data):
    return False
  
  def read(self):
    return False
  
  def request(self, data):
    """Writes the packet to the interface, then listens for and returns
    a response
    
    :param data: packet to write
    :type data: :class:`alphasign.packet.Packet`
    :returns: string containing the data. False if there was an error with the read or write.
    """
    
    if self.write(data):
      return self.read()
    return False

  def clear_memory(self):
    """Clear the sign's memory.

    :rtype: None
    """
    pkt = packet.Packet("%s%s" % (constants.WRITE_SPECIAL, "$"))
    self.write(pkt)
    time.sleep(1)

  def beep(self, frequency=0, duration=0.1, repeat=0):
    """Make the sign beep.

    :param frequency: frequency integer (not in Hz), 0 - 254
    :param duration: beep duration, 0.1 - 1.5
    :param repeat: number of times to repeat, 0 - 15

    :rtype: None
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

    pkt = packet.Packet("%s%s%02X%X%X" % (constants.WRITE_SPECIAL, "(2",
                                          frequency, duration, repeat))
    self.write(pkt)

  def soft_reset(self):
    """Perform a soft reset on the sign.

    This is non-destructive and does not clear the sign's memory.

    :rtype: None
    """
    pkt = packet.Packet("%s%s" % (constants.WRITE_SPECIAL, ","))
    self.write(pkt)

  def allocate(self, files):
    """Allocate a set of files on the device.

    :param files: list of file objects (:class:`alphasign.text.Text`,
                                        :class:`alphasign.string.String`, ...)

    :rtype: None
    """
    seq = ""
    for obj in files:
      size_hex = "%04X" % obj.size
      # format: FTPSIZEQQQQ

      if type(obj) == alphasign.string.String:
        file_type = "B"
        qqqq = "0000"  # unused for strings
        lock = constants.LOCKED
      else:  # if type(obj) == alphasign.text.Text:
        file_type = "A"
        qqqq = "FFFF"  # TODO(ms): start/end times
        lock = constants.UNLOCKED

      alloc_str = ("%s%s%s%s%s" %
                   (obj.label,  # file label to allocate
                   file_type,   # file type
                   lock,
                   size_hex,    # size in hex
                   qqqq))
      seq += alloc_str

    # allocate special TARGET TEXT files 1 through 5
    for i in range(5):
      alloc_str = ("%s%s%s%s%s" %
                   ("%d" % (i + 1),
                   "A",    # file type
                   constants.UNLOCKED,
                   "%04X" % 100,
                   "FEFE"))
      seq += alloc_str

    pkt = packet.Packet("%s%s%s" % (constants.WRITE_SPECIAL, "$", seq))
    self.write(pkt)

  def set_run_sequence(self, files, locked=False):
    """Set the run sequence on the device.

    This determines the order in which the files are displayed on the device, if
    at all. This is useful when handling multiple TEXT files.

    :param files: list of file objects (:class:`alphasign.text.Text`,
                                        :class:`alphasign.string.String`, ...)
    :param locked: allow sequence to be changed with IR keyboard

    :rtype: None
    """
    seq_str = ".T"
    seq_str += locked and "L" or "U"
    for obj in files:
      seq_str += obj.label
    pkt = packet.Packet("%s%s" % (constants.WRITE_SPECIAL, seq_str))
    self.write(pkt)
    
  @staticmethod
  def _decorate_table_entry(entry):
    """Add processed attributes to a table entry retrieved from the read_memory_table function below
    
    This function adds some processed attributes to each table entry- it adds
    a human-readable data type, parses the size into height and width for dots
    pictures, and converts the size to an int. It returns a new entry, and
    leaves the old one untouched.
    
    :param entry: the table entry to decorate
    :returns: the decortated table entry
    """
    
    result = dict(entry.iteritems())
    
    #convert size from hex string to int
    result["size"] = int(result["size"], 16)
    
    #add type field. add height and width for dots.
    if result["type character"] == "A":
      result["type"] = "TEXT"
    elif result["type character"] == "B":
      result["type"] = "STRING"
    elif result["type character"] == "D":
      result["type"] = "DOTS"
      #additionally add height and width
      result["height"] = int(result["size"] / 256)
      result["width"] = result["size"] % 256
      
    return result
  
  @staticmethod
  def _chunk_raw_memory_table(table):
    """Simple generator to split a raw memory table into 11-character entries
    """
    for i in xrange(0, len(table), 11):
      yield table[i:i+11]
      
  def read_raw_memory_table(self):
    """Reads the current memory configuration as a raw string
    
    This function reads the raw memory configuration from the sign, extracts
    the data table portion, and returns it raw. 
    
    :returns: raw memory layout. False if there was an error in the process.
    """
    memory = self.request(packet.Packet('F$'))
    if memory == False or memory == '':
      return False
    
    #TODO: checksum verification
    
    #This pattern extracts the table and checksum from the packet
    pattern = "\x00+\x01000\x02E\$(?P<table>(?:[\x20-\x7F][ABD][UL][0-9A-Fa-f]{4}[0-9A-Fa-f]{4})*)\x03(?P<checksum>[0-9A-Fa-f]{4})\x04"
    match = re.match(pattern, memory)
    if match is not None:
      return match.group('table')
    else:
      return False
  
  def read_memory_table(self, table=None):
    """Read and parse the current memory table
    
    This function reads the current memory table and parses it into a list of
    dicts, where each dict contains the configuration for a single file label.
    If the table argument is given, it is used instead of reading from the sign.
    
    Example: `sign.read_memory_table(sign.read_raw_memory_table())` is the same
    as `sign.read_memory_table()`
    
    :param table: an optional string containing a raw memory layout, such as
      is outputted by read_raw_memory_table()
    :returns: list of dicts, where each dict is the data for a single file in the table
    """
    
    if table is None:
      table = self.read_raw_memory_table()
      
    if table == False:
      return False
    
    pattern = re.compile("(?P<label>[\x20-\x7F])(?P<type>[ABD])(?P<locked>[UL])(?P<size>[0-9a-fA-F]{4})(?P<Q>[0-9A-Fa-f]{4})")
    
    table = self._chunk_raw_memory_table(table) #table is split into 11 character entries
    table = imap(pattern.match, table) #each entry is matched to the memory-table-entry regex
    table = imap(lambda match: match.groupdict(), table) #the groups and their values are extracted from the match
    table = imap(self._decorate_table_entry, table) #the group dicts are decorated, to make them more human readable
    
    return list(table)
