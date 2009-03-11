import serial
import time

from alphasign.interfaces import base


class Serial(base.BaseInterface):
  def __init__(self, device="/dev/ttyS0"):
    self.device = device
    self.debug = True

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

  def write(self, packet):
    if not self._conn:
      return
    if self.debug:
      print "Writing packet: %s" % repr(packet)
    self._conn.write(str(packet))


class DebugInterface(base.BaseInterface):
  def __init__(self):
    self.debug = True

  def connect(self):
    pass

  def disconnect(self):
    pass

  def write(self, packet):
    if self.debug:
      print "Writing packet: %s" % repr(packet)

