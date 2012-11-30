"""
The following constants are defined to change TEXT
(:class:`alphasign.text.Text`) colors:

* :const:`RED`
* :const:`GREEN`
* :const:`AMBER`
* :const:`DIM_RED`
* :const:`DIM_GREEN`
* :const:`BROWN`
* :const:`ORANGE`
* :const:`YELLOW`
* :const:`RAINBOW_1`
* :const:`RAINBOW_2`
* :const:`COLOR_MIX`
* :const:`AUTOCOLOR`

.. autofunction:: rgb
.. autofunction:: shadow_rgb

--------
Examples
--------

Make a text file with red text::

  msg = alphasign.Text("%sthis text is red" % alphasign.colors.RED, label="A")

Make a text file with purple text (#CC66FF)::

  msg = alphasign.Text("%sthis text should be in purple" %
                       alphasign.colors.rgb("CC66FF"), label="A")

Make a bi-color text file (red primary with a green shadow)::

  msg = alphasign.Text("%s%sred and green" %
                       (alphasign.colors.rgb("FF0000"),
                        alphasign.colors.rgb("00FF00")), label="A")
"""

# Colors
RED       = "\x1C1"
GREEN     = "\x1C2"
AMBER     = "\x1C3"
DIM_RED   = "\x1C4"
DIM_GREEN = "\x1C5"
BROWN     = "\x1C6"
ORANGE    = "\x1C7"
YELLOW    = "\x1C8"
RAINBOW_1 = "\x1C9"
RAINBOW_2 = "\x1CA"
COLOR_MIX = "\x1CB"
AUTOCOLOR = "\x1CC"

# Colors for SMALL DOTS / LARGE DOTS pictures
DOTS_BLANK = "\x30"
DOTS_RED = "\x31"
DOTS_GREEN = "\x32"
DOTS_AMBER = "\x33"
DOTS_DIM_RED = "\x34"
DOTS_DIM_GREEN = "\x35"
DOTS_BROWN = "\x36"
DOTS_ORANGE = "\x37"
DOTS_YELLOW = "\x38"

def rgb(rgb):
  """
  Create color constant for use in TEXT and STRING files.

  :param rgb: 6-character hex string in form RRGGBB.
  """
  if len(rgb) and rgb[0] == "#":
    rgb = rgb[1:]
  return "\x1CZ%s" % rgb


def shadow_rgb(rgb):
  """
  Create shadow color constant for use in TEXT and STRING files.

  :param rgb: 6-character hex string in form RRGGBB.
  """
  if len(rgb) and rgb[0] == "#":
    rgb = rgb[1:]
  return "\x1CY%s" % rgb
