"""
This module defines positions for use in TEXT files.

The following position constants are defined:

* :const:`MIDDLE_LINE`
* :const:`TOP_LINE`
* :const:`BOTTOM_LINE`
* :const:`FILL`
* :const:`LEFT`
* :const:`RIGHT`

:const:`LEFT` and :const:`RIGHT` only work on Alpha 3.0 protocol signs.

Conditions and exceptions for these positions are described in Section 7.10 of
the Alpha Sign Communications Protocol document.
"""

# Display positions
MIDDLE_LINE = "\x20"
TOP_LINE    = "\x22"
BOTTOM_LINE = "\x26"
FILL        = "\x30"
LEFT        = "\x31"
RIGHT       = "\x32"
