#!/usr/bin/perl -w
use warnings;
use strict;
use Authen::Passphrase::BlowfishCrypt;
use DBI;
use Time::HiRes qw/ time /;

## Usage :
# ex : ./race_condition.pl register admin password123
# ex : ./race_condition.pl login admin password123

my $startTime = time;

## check params
if(@ARGV != 3 || !$ARGV[0] || !$ARGV[1] || !$ARGV[2]){
    print "Please send me an 'action' (register or login) with your credentials (login, then password)\n";
    exit 0;
}
my $action = $ARGV[0];
my $login = $ARGV[1];
my $passwd = $ARGV[2];
## end check params

my $driver = "SQLite";
my $dsn = "DBI:$driver:dbname=/tmp/race_condition.db";
my $dbh = DBI->connect($dsn, undef, undef, { sqlite_see_if_its_a_number => 1, AutoCommit => 1 }) or exit;


sub getUserId{
	my $sth = $dbh->prepare("SELECT id, password FROM users WHERE login=?");
	$sth->bind_param(1, $login);
	$sth->execute;
	$sth->bind_columns(\my($id, $hashedPass));
	my $user = $sth->fetchrow_array;
	if($user){
		my $passphrase = Authen::Passphrase::BlowfishCrypt->from_crypt($hashedPass);
		if($passphrase->match($passwd)) {
			return $id;
		}
	}
	return -1;
}


sub doRegister{
	my $hashedPasswd = Authen::Passphrase::BlowfishCrypt->new( cost=> 8, salt_random => 1, passphrase => $passwd);
	my $sth = $dbh->prepare("INSERT INTO users(login, password) VALUES(?, ?)");
	$sth->bind_param(1, $login);
	$sth->bind_param(2, $hashedPasswd->as_crypt);
	$sth->execute or exit;
	select(undef, undef, undef, 0.5); # simulate more db access / calculus
	my $elapsed = time - $startTime;
	print("It's been " . $elapsed . "s since you started register.\n");
	$sth = $dbh->prepare("INSERT INTO forbidden_ids(user_id) VALUES(?)");
	$sth->execute(getUserId()) or exit;
}


sub doLogin{
	my $userId = getUserId();
	if ($userId < 0){
		return "We failed to log you in :/\n";
	}
	my $sth = $dbh->prepare("SELECT count(*) FROM forbidden_ids WHERE user_id=?");
	my $elapsed = time - $startTime;
	print("It's been " . $elapsed ."s since you started log in.\n");
	$sth->execute($userId) or exit;
	$sth->bind_columns(\my($count));
	$sth->fetchrow_array;
	if($count > 0){
		return "You are logged in. But sorry you are not allowed to see the secret.\n";
	}
	open my $fh, '<', 'secret' or die "error opening secret file";
	my $secret = do { local $/; <$fh> };
	return "You are logged in. And congratz ! Here is the secret : " . $secret . "\n";
}


if ($action eq 'register'){
	doRegister();
	print "You are registered !\n";
}elsif($action eq 'login'){
	print doLogin();
}else{
	print "Error, action param not valid.\n";
}

$dbh->disconnect();

1;
