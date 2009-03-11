# Display Modes (p89)
modes = {
  "rotate":             "a",
  "hold":               "b",
  "flash":              "c",
  "roll_up":            "e",
  "roll_down":          "f",
  "roll_left":          "g",
  "roll_right":         "h",
  "wipe_up":            "i",
  "wipe_down":          "j",
  "wipe_left":          "k",
  "wipe_right":         "l",
  "scroll":             "m",
  "automode":           "o",
  "roll_in":            "p",
  "roll_out":           "q",
  "wipe_in":            "r",
  "wipe_out":           "s",
  "compressed_rotate":  "t",  # only available on certain sign models
  "explode":            "u",  # alpha 3.0 protocol
  "clock":              "v",  # alpha 3.0 protocol
  # Special Modes
  "twinkle":            "n0",
  "sparkle":            "n1",
  "snow":               "n2",
  "interlock":          "n3",
  "switch":             "n4",
  "slide":              "n5",  # only Betabrite 1036 (same as CYCLE_COLORS?)
  "spray":              "n6",
  "starburst":          "n7",
  "welcome":            "n8",
  "slot_machine":       "n9",
  "news_flash":         "nA",  # only Betabrite 1036
  "trumpet_animation":  "nb",  # only betabrite 1036
  "cycle_colors":       "nC",  # only AlphaEclipse 3600
  # Special Graphics (these display before the message)
  "thank_you":          "nS",
  "no_smoking":         "nU",
  "dont_drive_drive":   "nV",
  "running_animal":     "nW",
  "fish_animation":     "nW",
  "fireworks":          "nX",
  "turbo_car":          "nY",
  "balloon_animation":  "nY",
  "cherry_bomb":        "nZ",
}

# Display Positions
positions = {
  "middle_line":        "\x20",
  "top_line":           "\x22",
  "bottom_line":        "\x26",
  "fill":               "\x30",
  "left":               "\x31",
  "right":              "\x32",
}


# Counters
# We have 5 of them.
counters = {
  1:                    "z",
  2:                    "{",
  3:                    "|",
  4:                    "}",
  5:                    "-",
}



# Command Codes
WRITE_TEXT            = "A"  # Write TEXT file (p18)
READ_TEXT             = "B"  # Read TEXT file (p19)
WRITE_SPECIAL         = "E"  # Write SPECIAL FUNCTION commands (p21)
READ_SPECIAL          = "F"  # Read SPECIAL FUNCTION commands (p29)
WRITE_STRING          = "G"  # Write STRING (p37)
READ_STRING           = "H"  # Read STRING (p38)
WRITE_SMALL_DOTS      = "I"  # Write SMALL DOTS PICTURE file (p39)
READ_SMALL_DOTS       = "J"  # Read SMALL DOTS PICTURE file (p41)
WRITE_RGB_DOTS        = "K"  # Write RGB DOTS PICTURE file (p44)
READ_RGB_DOTS         = "L"  # Read RGB DOTS PICTURE file (p46)
WRITE_LARGE_DOTS      = "M"  # Write LARGE DOTS PICTURE file (p42)
READ_LARGE_DOTS       = "N"  # Read LARGE DOTS PICTURE file (p43)
WRITE_ALPHAVISION     = "O"  # Write ALPHAVISION BULLETIN (p48)
SET_TIMEOUT           = "T"  # Set Timeout Message (p118) (Alpha 2.0/3.0)

# Constants used in transmission packets
NUL                   = "\x00"  # NULL
SOH                   = "\x01"  # Start of Header
STX                   = "\x02"  # Start of TeXt (precedes a command code)
ETX                   = "\x03"  # End of TeXt
EOT                   = "\x04"  # End Of Transmission
#ENQ                   = "\x05"  # Enquiry
#ACK                   = "\x06"  # Acknowledge
BEL                   = "\x07"  # Bell
BS                    = "\x08"  # Backspace
HT                    = "\x09"  # Horizontal tab
LF                    = "\x0A"  # Line Feed
NL                    = "\x0A"  # New Line
VT                    = "\x0B"  # Vertical Tab
#FF                    = "\x0C"  # Form Feed
#NP                    = "\x0C"  # New Page
CR                    = "\x0D"  # Carriage Return
CAN                   = "\x18"  # Cancel
SUB                   = "\x1A"  # Substitute (select charset)
ESC                   = "\x1B"  # Escape character
