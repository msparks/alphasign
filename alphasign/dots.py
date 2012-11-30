from packet import Packet
import colors
import constants

class Dots(object):
  """Class reperesenting a SMALL DOTS file.
  
  :ivar data: list containing the pixel data
  :ivar rows: the number of rows in the image
  :ivar columns: the number of columns in the image
  :ivar label: the label of the dots object
  """
  
  def __init__(self, rows=None, columns=None, fill=None, label=None):
    """
    :param rows: the number of rows in the image (default: 32)
    :param columns: the number of columns in the image (default: 255)
    :param fill: the color to fill the sign with (default: DOTS_BLANK)
    """
    #The defaults here are the resolution of the alpha big dot sign. I'm not
    #familiar with other sizes, but I'm open to more common defaults
    if rows in None:
      rows = 7
    if columns is None:
      columns = 80 
    if fill is None:
      fill = colors.DOTS_BLANK
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
    
    self.columns = columns
    self.rows = rows
    self.data = [fill for _ in xrange(rows * columns)]
    self.label = label
    
    #Size is stored such that in can be unpacked as two 2-byte hex numbers
    self.size = (rows * 256) + columns
    
  def call(self):
    """Call a SMALL DOTS picture
    
    This is for inserting a DOTS file into a TEXT file
    
    :returns: control code and label
    :rtype: string
    """
    
    return "\x14%s" % self.label
  
  def __str__(self):
    rows = [''.join(self.data[row:row+self.columns]) for row in xrange(0, self.rows * self.columns)]
    data = ''.join(('%s%s' % (row, constants.CR) for row in rows))
    hex_size = "%04x" % self.size
    
    return str(Packet("%s%s%s%s" %
      (constants.WRITE_SMALL_DOTS,
       self.label,
       hex_size,
       data)))
    
    def __repr__(self):
      return repr(self.__str__())
    
    def _getindex(row, column):
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
      index = self._getindex(*key)
      self.data[index] = value
      
    def __getitem__(self, key):
      """Get the value of a pixel
      
      :param key: a tuple of (row, column)
      :raises: IndexError if key outside the row, column range
      :raises: TypeError if key is not a tuple
      """
      if type(key) != tuple:
        raise TypeError("key must be a tuple")
      index = self._getindex(*key)
      return self.data[index]
    