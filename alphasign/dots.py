from packet import Packet
import dotcolors
import constants

class Dots(object):
  """Class reperesenting a SMALL DOTS file.
  
  :ivar data: bytearray containing the pixel data
  :ivar rows: the number of rows in the image
  :ivar columns: the number of columns in the image
  :ivar label: the label of the dots object
  :ivar size: a combined representation of rows and columns, for the interface allocator
  """
  
  def __init__(self, rows=None, columns=None, fill=None, label=None):
    """
    :param rows: the number of rows in the image (default: 7)
    :param columns: the number of columns in the image (default: 80)
    :param fill: the color to fill the sign with (default: BLANK)
    """
    #The defaults here are the resolution of the alpha big dot sign. I'm not
    #familiar with other sizes, but I'm open to more common defaults
    if rows is None:
      rows = 7
    if columns is None:
      columns = 80 
    if fill is None:
      fill = dotcolors.BLANK
    if label is None:
      label = "1" #TODO: find a reasonable default
    
    if rows > 31:
      rows = 31
    if columns < 1:
      columns = 1
    if columns > 255:
      columns = 255
    if columns < 1:
      columns = 1
    
    #extra column for the <CR> bytes
    columns = columns + 1
    
    self.columns = columns
    self.rows = rows
    self.data = bytearray(fill for _ in xrange(rows * columns))
    #write the <CR> characters
    for row in xrange(self.rows):
      self[(row, columns - 1)] = constants.CR
    self.label = label
    
    #Size is stored such that in can be unpacked as two 2-byte hex numbers by allocate
    self.size = (rows * 256) + (columns - 1)
    
  def call(self):
    """Call a SMALL DOTS picture
    
    This is for inserting a DOTS file into a TEXT file
    
    :returns: control code and label
    :rtype: string
    """
    
    return "\x14%s" % self.label
  
  def __str__(self):
    hex_size = "%04x" % self.size
    
    return str(Packet("%s%s%s%s" %
      (constants.WRITE_SMALL_DOTS,
       self.label,
       hex_size,
       self.data)))
    
  def __repr__(self):
    return repr(self.__str__())
  
  def _getindex(self, row, column):
    if row < 0 or row >= self.rows:
      raise IndexError("row must be in the range [0, %s)" % self.rows)
    if column < 0 or column >= self.columns:
      raise IndexError("column must be in the range [0, %s)" % self.columns)
    return (row * self.columns) + column
  
  def __setitem__(self, key, value):
    """Set an individual pixel
    
    :param key: a tuple of (row, column)
    :param value: the value to set the pixel to
    :raises: IndexError if key outside the row, column range
    :raises: TypeError if key is not a tuple
    """
    if type(key) != tuple:
      raise TypeError("key must be a tuple")
    self.data[self._getindex(*key)] = value
    
  def __getitem__(self, key):
    """Get the value of a pixel
    
    :param key: a tuple of (row, column)
    :raises: IndexError if key outside the row, column range
    :raises: TypeError if key is not a tuple
    """
    if type(key) != tuple:
      raise TypeError("key must be a tuple")
    return self.data[self._getindex(*key)]
  
  def debug_print(self):
    """Prints the currently stored image
    """
    for row in xrange(self.rows):
      begin = self._getindex(row, 0)
      end = self._getindex(row, self.columns - 1)
      print self.data[begin:end]
      
  def set_row(self, row_index, row, fill=dotcolors.BLANK):
    """Sets the row at row_index to the string specified by row
    
    This functions sets a row. If row is shorter than the width, it is padded
    on the right the fill parameter. If it is longer, it is truncated on the
    right.
    
    :param row_index: the index of the row to set
    :param row: a string with the row fill data
    :param fill: optional parameter specifying the fill parameter
    """
    
    real_columns = self.columns-1
    
    if len(row) < real_columns:
      row = row.ljust(real_columns, fillchar=fill)
    elif len(row) > real_columns:
      row = row[:real_columns]
    row = row + constants.CR
    
    self.data[self.columns * row_index:self.columns * (row_index + 1)] = row
