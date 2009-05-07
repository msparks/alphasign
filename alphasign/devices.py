"""
Device constants are used during instantiation of interface classes (such as
:class:`alphasign.interfaces.local.USB`) to describe particular sign devices.

The following constants are defined in this module:

* :const:`USB_BETABRITE_PRISM` = (0x8765, 0x1234)

--------
Examples
--------

Connect to a BetaBrite Prism sign using USB::

  sign = alphasign.USB(alphasign.devices.USB_BETABRITE_PRISM)
  sign.connect()
  ...
"""

USB_BETABRITE_PRISM = (0x8765, 0x1234)
