#!/usr/bin/perl -w
use warnings;
use strict;

## check params
my $directory = $ARGV[0];
if ($directory !~ /[a-zA-Z0-9_\/-]+/){
    print "Error, directory param not valid.";
    exit 1;
}
## end check params

## write configuration file
my @chars = ("A".."Z", "a".."z", "0".."9");
my $fileName = "/srv/writable/";
$fileName .= $chars[rand @chars] for 1..30;
open(my $fh, '>', $fileName) or die "Could not open file '$fileName' $!";
print $fh "/bin/mkdir $directory\n";
print $fh "/bin/touch $directory/folder_configured\n";
print $fh "exit 0\n";
close $fh;
## end write configuration file

## call configuration
system("/bin/sh $fileName");
## end call configuration

if (-e $directory){
    print "Directory configured\n";
}else{
    print "Failed to configure directory\n";
}

1;
