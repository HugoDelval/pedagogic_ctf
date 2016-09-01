#!/usr/bin/perl -w
use warnings;
use strict;

## Usage :
# ./injection_conf.pl <directory_path>
# ex: ./injection_conf.pl /tmp/test
# create a config file (configurationFileName) containing a variable which value is set to <directory_path>
# then create a project based on this configuration file

## check params
if (@ARGV == 0 || !$ARGV[0]) {
	print "Please send me a directory path so I can launch my configuration script !\n";
	exit 0;
}
my $directory = $ARGV[0];
if ($directory !~ /(\/tmp\/|\/srv\/writable\/)[a-zA-Z0-9_-]+/){
    print "Error, directory param not valid.\n";
    exit 0;
}
if (-e $directory){
    print "Directory already exists.\n";
    exit 0;
}
## end check params

## write configuration file
my @chars = ("A".."Z", "a".."z", "0".."9");
my $configurationFileName = "/srv/writable/";
$configurationFileName .= $chars[rand @chars] for 1..30;
$configurationFileName .= "_config.sh";
open(my $fh, '>', $configurationFileName) or die "Could not open file '$configurationFileName' $!";
print $fh "DATE=`date`\n";
print $fh "DIRECTORY=$directory\n";
close $fh;
## end write configuration file

## create project based on the config file
my $command = ". $configurationFileName && ";
$command .= 'mkdir "${DIRECTORY}" && ';
$command .= 'echo ${DATE} > "${DIRECTORY}/folder_configured"';
system($command);
## end create project based on the config file

if (-e $directory){
    print "Directory configured.\n";
}else{
    print "Failed to configure directory.\n";
}

1;
