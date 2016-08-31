#!/usr/bin/perl -w
use warnings;
use strict;

## check params
if (@ARGV == 0 || !$ARGV[0]) {
	print "Please send me a server address so I can dig it ! (ex: 127.0.0.1 or www.ovh.com)\n";
	exit 0;
}
my $server = $ARGV[0];
if ($server =~ /!;&|'"`\${}></){
    print "Error, server param not valid.\n";
    exit 0;
}
## end check params

## launch dig
my $resultDig = `/usr/bin/dig $server`;
## end launch dig

print "$resultDig\n";

1;
