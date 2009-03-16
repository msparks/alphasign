import serial
import time

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

  def connect(self):
    """Establish connection to the device.
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
    """Disconnect from the device.
    """
    if self._conn:
      self._conn.close()

  def write(self, packet):
    """Write packet to the serial interface.

    :param packet: packet to write
    :type packet: :class:`alphasign.packet.Packet`
    """
    if not self._conn:
      return
    if self.debug:
      print "Writing packet: %s" % repr(packet)
    self._conn.write(str(packet))


class DebugInterface(base.BaseInterface):
  """Dummy interface used only for debugging.

  This does nothing except print the contents of written packets.
  """
  def __init__(self):
    self.debug = True

  def connect(self):
    pass

  def disconnect(self):
    pass

  def write(self, packet):
    if self.debug:
      print "Writing packet: %s" % repr(packet)

