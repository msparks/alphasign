import serial
import time
import usb

from alphasign.interfaces import base


class Serial(base.BaseInterface):
  """Connect to a sign through a local serial device.

  This class uses `pySerial <http://pyserial.sourceforge.net/>`_.
  """
  def __init__(self, device="/dev/ttyS0"):
    """
    :param device: character device (default: /dev/ttyS0)
    :type device: string
    """
    self.device = device
    self.debug = True
    self._conn = None

  def connect(self):
    """Establish connection to the device.
    """
    # TODO(ms): these settings can probably be tweaked and still support most of
    # the devices.
    self._conn = serial.Serial(port=self.device,
                               baudrate=4800,
                               parity=serial.PARITY_EVEN,
                               stopbits=serial.STOPBITS_TWO,
                               bytesize=serial.SEVENBITS,
                               timeout=1,
                               xonxoff=0,
                               rtscts=0)

  def disconnect(self):
    """Disconnect from the device.
    """
    if self._conn:
      self._conn.close()

  def write(self, packet):
    """Write packet to the serial interface.

    :param packet: packet to write
    :type packet: :class:`alphasign.packet.Packet`
    """
    if not self._conn or not self._conn.isOpen():
      self.connect()
    if self.debug:
      print "Writing packet: %s" % repr(packet)
    try:
      self._conn.write(str(packet))
    except OSError:
      return False
    else:
      return True
    
  def read(self):
    """Read a response from the serial interface.
    
    :returns: string containing the data. False if there was an error.
    """
    
    if not self._conn or not self._conn.isOpen():
      self.connect()
    if self.debug:
      print "Reading packet: ",
    try:
      result = self._conn.readall()
    except OSError:
      return False
    print result
    return result
  
  


class USB(base.BaseInterface):
  """Connect to a sign using USB.

  This class uses `PyUSB <http://pyusb.berlios.de>`_.
  """
  def __init__(self, usb_id):
    """
    :param usb_id: tuple of (vendor id, product id) identifying the USB device
    """
    self.vendor_id, self.product_id = usb_id
    self.debug = False
    self._handle = None
    self._conn = None

  def _get_device(self):
    for bus in usb.busses():
      for device in bus.devices:
        if (device.idVendor == self.vendor_id and
            device.idProduct == self.product_id):
          return device
    return None

  def connect(self, reset=True):
    """
    :param reset: send a USB RESET command to the sign.
                  This seems to cause problems in VMware.
    :exception usb.USBError: on USB-related errors
    """
    if self._conn:
      return

    device = self._get_device()
    if not device:
      raise usb.USBError, ("failed to find USB device %04x:%04x" %
                           (self.vendor_id, self.product_id))

    interface = device.configurations[0].interfaces[0][0]
    self._read_endpoint, self._write_endpoint = interface.endpoints
    self._conn = device.open()
    if reset:
      self._conn.reset()
    self._conn.claimInterface(interface)

  def disconnect(self):
    """ """
    if self._conn:
      self._conn.releaseInterface()

  def write(self, packet):
    """ """
    if not self._conn:
      self.connect()
    if self.debug:
      print "Writing packet: %s" % repr(packet)
    written = self._conn.bulkWrite(self._write_endpoint.address, str(packet))
    if self.debug:
      print "%d bytes written" % written
    self._conn.bulkWrite(self._write_endpoint.address, '')
    
  def read(self):
    raise NotImplementedError("USB interface does not yet support reads")


class DebugInterface(base.BaseInterface):
  """Dummy interface used only for debugging.

  This does nothing except print the contents of written packets.
  """
  def __init__(self):
    self.debug = True

  def connect(self):
    """ """
    pass

  def disconnect(self):
    """ """
    pass

  def write(self, packet):
    """ """
    if self.debug:
      print "Writing packet: %s" % repr(packet)
    return True
  
  def read(self):
    if self.debug:
      print "Reading packet"
    return ''
