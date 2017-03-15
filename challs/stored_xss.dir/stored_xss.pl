#! /usr/bin/env perl

use strict;
use warnings;
use DBI;
use Digest::SHA  qw(sha1_hex);
use HTML::Defang;
use HTML::Scrubber;
use MIME::Base64;
use Mojolicious;
use Mojo::Log;
use Mojo::URL;
use Mojo::UserAgent;

my $driver = "SQLite";
my $dsn = "DBI:$driver:dbname=/tmp/stored_xss.db";
my $dbh = DBI->connect($dsn, undef, undef, { sqlite_see_if_its_a_number => 1, AutoCommit => 1 }) or exit;

my $email = "";
my $app = Mojolicious->new;
$app = $app->log(Mojo::Log->new(path => '/dev/null'));


$app->routes->post('/comments' => sub {
    #
    #    Create or update token for current user
    #
    my $c = shift;
    my $comment = $c->param('comment');
    my $sth = $dbh->prepare("INSERT INTO comments(author, comment) VALUES(?,?)");
    $sth->bind_param(1, $email);
    $sth->bind_param(2, $comment);
    $sth->execute;
    
    return $c->render(
        status => 200,
        text => "Your comment has been inserted"
    );
});

$app->routes->get('/comments' => sub {
    #
    #    Return secret page
    #
    my $c = shift;
    my $sth = $dbh->prepare("SELECT author, comment from comments");
    $sth->execute();
        
    my $response = "<table><tr><th>Author</th><th>comment</th></tr>";

    while(my @row = $sth->fetchrow_array()) {
        $response = $response . "<tr><td>$row[0]</td><td>$row[1]</td></tr>";
    }

    $response = $response . "</table>";
    return $c->render(
        status => 200, 
        text => $response
    );
});

####################     Main   #############################

sub main {

    $email = $ARGV[0];
    my $comment = $ARGV[1];

    if (!$comment) {
        print "Missing comment";
        exit 0;
    }
    
    my $url = Mojo::URL->new("/comments");
    my $ua = Mojo::UserAgent->new();
    $ua->server->app($app);
    $ua->post($url => form => {comment => $comment});
    my $output = `python3 victim_browser.py $email`;
    print $output;
}

main();
1;

__DATA__

@@ not_found.html.ep
% layout 'default';
<h1>Not found</h1>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <head><title>MyApp</title></head>
  <body><%= content %></body>
</html>
