from alphasign import constants
from alphasign import packet


class BaseInterface(object):
  def write(self, data):
    pass

  def clear_memory(self):
    """Clear the sign's memory.
    """
    pkt = packet.Packet("%s%s" % (constants.WRITE_SPECIAL, "$"))
    self.write(pkt)

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

    pkt = packet.Packet("%s%s%02X%X%X" % (constants.WRITE_SPECIAL, "(2",
                                          frequency, duration, repeat))
    self.write(pkt)

  def soft_reset(self):
    """Perform a soft reset on the sign.

    This is non-destructive and does not clear the sign's memory.
    """
    pkt = packet.Packet("%s%s" % (constants.WRITE_SPECIAL, ","))
    self.write(pkt)
