#!/usr/bin/perl
use strict;
use Ezkey;
use Date::Format qw/time2str/;

my $sign=new Ezkey("/dev/rfcomm0");
$sign->connect();

$sign->set_mode("hold");
$sign->create_string("1",12);
$sign->write_text($sign->spacing(1)
                  .$sign->color("green").$sign->extchar("right_arrow")." "
                  .$sign->color("red")
                  .$sign->call_string(1));

while(1) {
    my $text=time2str("%d.%H%M%S",time);
    $sign->write_string($text);
    sleep 1;
}

$sign->disconnect();
