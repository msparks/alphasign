import constants


class Packet(object):
  def __init__(self, contents):
    self.type     = "Z"            # Type Code (see protocol)
    self.address  = "00"           # Sign Address (see protocol)
    self._pkt = ("%s%s%s%s%s%s%s" %
                 (constants.NUL * 5, constants.SOH, self.type,
                  self.address, constants.STX, contents,
                  constants.EOT))

  def __str__(self):
    return self._pkt

  def __repr__(self):
    return repr(self._pkt)

