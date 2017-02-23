#!/usr/bin/perl -w
use warnings;
use strict;

## Usage :
# ./command_injection.pl <server_address>
# ex: ./command_injection.pl www.ovh.com
# do a dig on this server

## check params
if (@ARGV == 0 || !$ARGV[0]) {
	print "Please send me a server address so I can dig it ! (ex: google.com or www.ovh.com)\n";
	exit 0;
}
my $server = $ARGV[0];
if ($server =~ /[!;&\|'"`\${}><]/){
    print "Error, server param not valid.\n";
    exit 0;
}
## end check params

## launch dig
my $resultDig = `/usr/bin/dig +short $server`;
## end launch dig

print "$resultDig\n";

1;
