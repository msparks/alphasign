#!/usr/bin/perl
# Ezkey.pm
# Interface to the Alpha Sign Communications Protocol, EZ KEY II
# See http://www.ams-i.com/Pages/97088061.htm
#
# The purpose of this interface is to objectify and simplify communication
# with LED signs like the BetaBrite: http://betabrite.com/
#
# @author Matt Sparks
package Ezkey;

use strict;
use Data::Dumper;
use IO::Handle;
use Date::Format;
use POSIX qw/floor/;

require Exporter;
our @ISA = qw/Exporter/;
our @EXPORT = qw/%modes %graphics %positions/;

# Display Modes (p89)
our %modes = (
  "rotate"            => "a",
  "hold"              => "b",
  "flash"             => "c",
  "roll_up"           => "e",
  "roll_down"         => "f",
  "roll_left"         => "g",
  "roll_right"        => "h",
  "wipe_up"           => "i",
  "wipe_down"         => "j",
  "wipe_left"         => "k",
  "wipe_right"        => "l",
  "scroll"            => "m",
  "automode"          => "o",
  "roll_in"           => "p",
  "roll_out"          => "q",
  "wipe_in"           => "r",
  "wipe_out"          => "s",
  "compressed_rotate" => "t",  # only available on certain sign models
  "explode"           => "u",  # alpha 3.0 protocol
  "clock"             => "v",  # alpha 3.0 protocol
  # Special Modes
  "twinkle"           => "n0",
  "sparkle"           => "n1",
  "snow"              => "n2",
  "interlock"         => "n3",
  "switch"            => "n4",
  "slide"             => "n5", # only Betabrite 1036 (same as CYCLE_COLORS?)
  "spray"             => "n6",
  "starburst"         => "n7",
  "welcome"           => "n8",
  "slot_machine"      => "n9",
  "news_flash"        => "nA", # only Betabrite 1036
  "trumpet_animation" => "nb", # only betabrite 1036
  "cycle_colors"      => "nC", # only AlphaEclipse 3600
  # Special Graphics (these display before the message)
  "thank_you"         => "nS",
  "no_smoking"        => "nU",
  "dont_drive_drink"  => "nV",
  "running_animal"    => "nW",
  "fish_animation"    => "nW",
  "fireworks"         => "nX",
  "turbo_car"         => "nY",
  "balloon_animation" => "nY",
  "cherry_bomb"       => "nZ",
);

# Display Positions
our %positions = (
  "middle_line"       => "\x20",
  "top_line"          => "\x22",
  "bottom_line"       => "\x26",
  "fill"              => "\x30",
  "left"              => "\x31",
  "right"             => "\x32",
);

# Character Sets
our %charsets = (
  "five_high_std"     => "1",
  "five_stroke"       => "2",
  "seven_high_std"    => "3",
  "seven_stroke"      => "4",
  "seven_high_fancy"  => "5",
  "ten_high_std"      => "6",
  "seven_shadow"      => "7",
  "full_height_fancy" => "8",
  "full_height_std"   => "9",
  "seven_shadow_fancy"=> ":",
  "five_wide"         => ";",
  "seven_wide"        => "<",
  "seven_fancy_wide"  => "=",
  "wide_stroke_five"  => ">",
  # The following four only work on Alpha 2.0 and Alpha 3.0 protocols
  "five_high_cust"    => "W",
  "seven_high_cust"   => "X",
  "ten_high_cust"     => "Y",
  "fifteen_high_cust" => "Z",
);

# Extended characters
our %extchars = (
  "up_arrow"          => "\x64",
  "down_arrow"        => "\x65",
  "left_arrow"        => "\x66",
  "right_arrow"       => "\x67",
  "pacman"            => "\x68",
  "sail_boat"         => "\x69",
  "ball"              => "\x6A",
  "telephone"         => "\x6B",
  "heart"             => "\x6C",
  "car"               => "\x6D",
  "handicap"          => "\x6E",
  "rhino"             => "\x6F",
  "mug"               => "\x70",
  "satellite_dish"    => "\x71",
  "copyright_symbol"  => "\x72",
  "male_symbol"       => "\x73",
  "female_symbol"     => "\x74",
  "bottle"            => "\x75",
  "diskette"          => "\x76",
  "printer"           => "\x77",
  "musical_note"      => "\x78",
  "infinity_symbol"   => "\x79",
);

# Counters
# We have 5 of them.
our %counters = (
  1                   => "z",
  2                   => "{",
  3                   => "|",
  4                   => "}",
  5                   => "-",
);

# Colors
our %colors = (
  "red"               => "1",
  "green"             => "2",
  "amber"             => "3",
  "dim_red"           => "4",
  "dim_green"         => "5",
  "brown"             => "6",
  "orange"            => "7",
  "yellow"            => "8",
  "rainbow_1"         => "9",
  "rainbow_2"         => "A",
  "color_mix"         => "B",
  "autocolor"         => "C",
);

# Command Codes
use constant {
  WRITE_TEXT          => "A", # Write TEXT file (p18)
  READ_TEXT           => "B", # Read TEXT file (p19)
  WRITE_SPECIAL       => "E", # Write SPECIAL FUNCTION commands (p21)
  READ_SPECIAL        => "F", # Read SPECIAL FUNCTION commands (p29)
  WRITE_STRING        => "G", # Write STRING (p37)
  READ_STRING         => "H", # Read STRING (p38)
  WRITE_SMALL_DOTS    => "I", # Write SMALL DOTS PICTURE file (p39)
  READ_SMALL_DOTS     => "J", # Read SMALL DOTS PICTURE file (p41)
  WRITE_RGB_DOTS      => "K", # Write RGB DOTS PICTURE file (p44)
  READ_RGB_DOTS       => "L", # Read RGB DOTS PICTURE file (p46)
  WRITE_LARGE_DOTS    => "M", # Write LARGE DOTS PICTURE file (p42)
  READ_LARGE_DOTS     => "N", # Read LARGE DOTS PICTURE file (p43)
  WRITE_ALPHAVISION   => "O", # Write ALPHAVISION BULLETIN (p48)
  SET_TIMEOUT         => "T", # Set Timeout Message (p118) (Alpha 2.0/3.0)
};

# Constants used in transmission packets
use constant {
  NUL                 => "\x00", # NULL
  SOH                 => "\x01", # Start of Header
  STX                 => "\x02", # Start of TeXt (precedes a command code)
  ETX                 => "\x03", # End of TeXt
  EOT                 => "\x04", # End Of Transmission
#   ENQ                 => "\x05", # Enquiry
#   ACK                 => "\x06", # Acknowledge
  BEL                 => "\x07", # Bell
  BS                  => "\x08", # Backspace
  HT                  => "\x09", # Horizontal tab
  LF                  => "\x0A", # Line Feed
  NL                  => "\x0A", # New Line
  VT                  => "\x0B", # Vertical Tab
#   FF                  => "\x0C", # Form Feed
#   NP                  => "\x0C", # New Page
  CR                  => "\x0D", # Carriage Return
  CAN                 => "\x18", # Cancel
  SUB                 => "\x1A", # Substitute (select charset)
  ESC                 => "\x1B", # Escape character
};

# Constructor
# - device: device of the LED sign
sub new {
  my($class,$device)=@_;

  my $self={
    "device"        => $device,
    "type"          => "Z",           # Type Code, see protocol
    "address"       => "00",          # Sign Address, see protocol
    "mode"          => "rotate",      # Default display mode
    "position"      => "middle_line", # Approrpriate for one-line signs
    "debug"         => 0,             # debugging
  };

  return bless $self,$class;
}

# Connect to the sign (open the serial device)
# If no device is known, the default /dev/ttyS0 is selected
sub connect {
  my($this,$device)=@_;
  $device ||= $this->{device};
  if (!$device) {
    warn "No device specified. Defaulting to /dev/ttyS0.\n";
    $device = "/dev/ttyS0";
  }

  # Open a connection to the sign
  open(OUT,">",$device)
    or die "Could not open $device for output: $!\n";
  OUT->autoflush(1);

  open(IN,"<",$device)
    or die "Could not open $device for input: $!\n";
  IN->autoflush(1);
}

# Disconnect from the sign (close the serial device)
sub disconnect {
  my($this)=@_;
  close OUT;
  close IN;
}

sub _packet {
  my($this,$contents)=@_;
  return ((NUL x 5) . SOH . $this->{type} . $this->{address} . STX
          . $contents . EOT);
}

sub _write {
  my($this,$packet)=@_;
  die "Not connected to device. Use \$sign->connect().\n" if !OUT->opened;
  if ($this->{debug}) {
    # make human-readable packet for display
    my $hr = $packet;
    #for(0..27) {
    #    my $hex = hex $_;
    #    $hr =~ s/\x$hex/[$hex]/g;
    #}
    print "Writing packet: $hr\n";
  }
  print OUT $packet;
}

# Read from the sign
# This does not seem to work correctly yet. All read_* functions therefore
# do not work.
sub _read {
  my($this)=@_;
  my $data;
  sysread IN,$data,1024;
  return $data;
}

sub dec2hex {
  my($dec) = @_;
  return sprintf("%lx ", $dec );
}

sub hex2dec {
  return hex($_[0]);
}

# Set display mode
# for $mode, use one of the Standard Mode constants exported
# if $mode is SPECIAL, set $special_mode to one of the defined special modes
sub set_mode {
  my($this,$mode)=@_;

  if ($modes{$mode}) {
    $this->{mode} = $mode;
  }
  else {
    warn "Warning: '$mode' is an invalid mode\n";
  }
}

# Get display mode
sub get_mode {
  my($this)=@_;
  return $this->{mode};
}

# Set display position
# This is mostly unimportant for one line signs.
sub set_position {
  my($this,$position)=@_;
  if ($positions{$position}) {
    $this->{position} = $position;
  }
  else {
    warn "Warning: '$position' is an invalid position\n";
  }
}

# Get display position
sub get_position {
  my($this)=@_;
  return $this->{position};
}

# Write TEXT to the sign
sub write_text {
  my($this,$msg,$label)=@_;
  $label ||= "A";

  # [WRITE_TEXT][File Label][ESC][Display Position][Mode Code]
  #   [Special Specifier][ASCII Message]
  my $packet = $this->_packet(WRITE_TEXT . $label . ESC
                              . $positions{$this->{position}}
                              . $modes{$this->{mode}} . $msg);
  $this->_write($packet);
}

# Read TEXT from the sign
sub read_text {
  my($this,$label)=@_;
  $label ||= "A";
  $this->_write($this->_packet(READ_TEXT . $label));
  return $this->_read();
}

# Create a STRING
# This is necessary to allocate memory for the STRING on the sign
#
# $string_label: label of the STRING to create
# $string_size:  size of the STRING to create, in bytes. 125 max.
#                Default is 32.
sub create_string {
  my($this,$string_label,$string_size)=@_;
  $string_label ||= 1;
  $string_size = 125 if $string_size > 125;
  $string_size ||= 32;
  my $size_hex = hex($string_size);
  $size_hex = "0"x(4-length($size_hex)).$size_hex if length($size_hex) < 4;
  my $packet = $this->_packet(WRITE_SPECIAL . "\$"
                              . "A"    # call label.. why does this matter?
                              . "A"    # text file type
                              . "U"    # this TEXT file is unlocked
                              . "0100" # text file size in hex
                              . "FF"   # text file's start time (FF = always)
                              . "00"   # text file's stop time
                              . $string_label
                              . "B"    # string file type
                              . "L"    # this string file is locked
                              . $size_hex
                              . "0000" # padding
                             );
  $this->_write($packet);
}

# Write a STRING
sub write_string {
  my($this,$data,$label)=@_;
  $label ||= 1;
  my $packet = $this->_packet(WRITE_STRING . $label . $data);
  $this->_write($packet);
}

sub read_string {
  my($this,$label)=@_;
  $label ||= 1;
  my $packet = $this->_packet(READ_STRING . $label);
  $this->_write($packet);
  return $this->_read();
}

# Call a STRING
# Returns the control code of specified string label. This is for
# inserting a STRING file into a TEXT file
sub call_string {
  my($this,$string_label)=@_;
  $string_label ||= "1";
  return "\x10" . $string_label;
}

# Call Date
# Returns the control code for the date to be inserted in a TEXT
# $format:  integer from 0 to 9
#           0 - MM/DD/YY
#           1 - DD/MM/YY
#           2 - MM-DD-YY
#           3 - DD-MM-YY
#           4 - MM.DD.YY
#           5 - DD.MM.YY
#           6 - MM DD YY
#           7 - DD MM YY
#           8 - MMM.DD, YYYY
#           9 - Day of week
# Format defaults to 0 if invalid or not specified
sub call_date {
  my($this,$format);
  $format ||= 0;
  $format = 0 if ($format < 0 || $format > 9);
  return "\x0B" . $format;
}

# Call Time
# Returns control code for the time.
sub call_time {
  my($this)=@_;
  return "\x13";
}

# Clear sign's memory
sub clear_memory {
  my($this)=@_;
  my $packet = $this->_packet(WRITE_SPECIAL . "\$");
  $this->_write($packet);
}

# Generate a tone/beep
#    $frequency: frequency of tone to generate, in hex ("00" through "FE")
#    $duration:  duration, in hex, of tone in 0.1s increments ("1" through "F")
#    $repeat:    number of times, in hex, to repeat the tone ("0" through "F")
sub beep {
  my($this,$frequency,$duration,$repeat)=@_;
  $frequency ||= "10";
  $duration  ||= "2";
  $repeat    ||= 0;

  my $packet = $this->_packet(WRITE_SPECIAL . "(2" . $frequency . $duration
                              . $repeat);
  $this->_write($packet);
}

# Perform a soft reset on the sign (does not clear memory; non-destructive)
sub soft_reset {
  my($this)=@_;
  my $packet = $this->_packet(WRITE_SPECIAL . ",");
  $this->_write($packet);
}

# Set the day of the week on the sign
# $day must be an integer between 1 and 7.
#    1 = Sunday, 2 = Monday, etc.
# Omitting the $day parameter will cause today's day to be sent
# Returns -1 if an invalid day is specified.
sub set_day {
  my($this,$day)=@_;
  return -1 if ($day && ($day < 1 || $day > 7));
  $day ||= time2str("%w",time)+1;

  my $packet = $this->_packet(WRITE_SPECIAL . "&" . $day);
  $this->_write($packet);
}

# Sets the date in the memory of the sign. This must be done each day to keep
# the clock 'up to date', because the sign will not automatically advance the
# day.
#
# NOTE: each of the parameters must be two characters long.
#
# If no date is specified, today's date will be used.
sub set_date {
  my($this,$year,$month,$day)=@_;
  $year  ||= time2str("%y",time);
  $month ||= time2str("%m",time);
  $day   ||= time2str("%d",time);

  my $packet = $this->_packet(WRITE_SPECIAL . ";" . $month . $day . $year);
  $this->_write($packet);
}

# Sets the hour and minute of the internal clock on the sign
# $h: hour in twenty-four hour format (18 instead of 6 for 6PM)
# $m: minute
# If no time (or an invalid time) is specified, the current system time will
# be used
sub set_time {
  my($this,$h,$m)=@_;
  $h = "" if ($h < 0 or $h > 23);
  $m = "" if ($m < 0 or $m > 59);
  $h ||= time2str("%H",time);
  $m ||= time2str("%M",time);

  my $packet = $this->_packet(WRITE_SPECIAL . "\x20" . $h . $m);
  $this->_write($packet);
}

# Sets the time format on the sign
# $format: 1 - 24-hour (military) time
#          0 - 12-hour (standard am/pm) format
# 12-hour is the default
sub set_time_format {
  my($this,$format)=@_;
  $format ||= 0;
  $format = 0 if ($format > 1 || $format < 0);
  my $byte = ($format == 0) ? "S" : "M";

  my $packet = $this->_packet(WRITE_SPECIAL . "\x27" . $byte);
  $this->_write($packet);
}

# Returns color code for a specified color
# If an invalid color is specified, autocolor will be used
sub color {
  my($this,$color)=@_;
  $color = "autocolor" if !$colors{$color};
  return "\x1C" . $colors{$color};
}

# Returns control code for a specified character set
# Defaults to 'five_high_std', Five High Standard
sub charset {
  my($this,$charset)=@_;
  $charset = "five_high_std" if !$charsets{$charset};
  return "\x1A" . $charsets{$charset};
}

# Returns control code for a specified extended char
# Defaults to 'left_arrow'
sub extchar {
  my($this,$extchar)=@_;
  $extchar = "left_arrow" if !$extchars{$extchar};
  return "\x08" . $extchars{$extchar};
}

# Returns control code to set the character spacing.
# $option: if 0, set proportional characters (default)
#             1, fixed width left justified characters
sub spacing {
  my($this,$option)=@_;
  my $byte = ($option == 0) ? 0 : 1;
  return "\x1E" . $byte;
}

# Set the speed
# $speed: integer 1 (slowest) through 5 (fastest) inclusive.
sub speed {
  my($this,$speed)=@_;
  $speed ||= 1;
  $speed = 1 if ($speed < 1 || $speed > 5);
  my $n = 20+$speed;
  return chr($n);
}

1;
