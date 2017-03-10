#! /usr/bin/env perl

use strict;
use warnings;
use DBI;
use Mojolicious;
use Mojo::Log;
use Mojo::URL;
use Mojo::UserAgent;

my $driver = "SQLite";
my $dsn = "DBI:$driver:dbname=/tmp/idor.db";
my $dbh = DBI->connect($dsn, undef, undef, { AutoCommit => 1 }) or exit;

my $username = "";
my $app = Mojolicious->new;
$app = $app->log(Mojo::Log->new(path => '/dev/null'));


sub getUserAccountDetails {
    #
    #    Get account details for user
    #
    my $accountId = shift;
    my $sth = $dbh->prepare("SELECT id, balance, description FROM accounts WHERE id=?");
    $sth->bind_param(1, $accountId);
    $sth->execute;
    $sth->bind_columns(\my($id, $balance, $desc));
    $sth->fetch;

    if (!$id) {
        return;
    }

    return "Account ID: $id,\nBalance:  $balance,\nDescription:  $desc";

}

$app->routes->get('/accounts/new' => sub {
    #
    #    Get account details for user
    #
    my $c = shift;
    my $defaultBalance = 100;
    
    my $sth = $dbh->prepare("INSERT OR REPLACE INTO accounts(username, balance) VALUES(?,?)");
    $sth->bind_param(1, $username);
    $sth->bind_param(2, $defaultBalance);
    $sth->execute;

    $sth = $dbh->prepare("SELECT id from accounts WHERE username=?");
    $sth->bind_param(1, $username);
    $sth->execute;
    my $accountId = $sth->fetchrow;

    my $response = "Your account $accountId has been successfully created.\nYou can view details here /accounts/$accountId/details";

    return $c->render(
        status => 200,
        text => $response
    );
});

$app->routes->get('/accounts/(:id)/details' => sub {
    #
    #    Return secret page
    #
    my $c = shift;
    my $accountId = $c->param('id');
    my $accountDetails = getUserAccountDetails($accountId);
        
    if (!$accountDetails) {
        return $c->render(
            status => 404,
            template => 'not_found_cust',
            content => "Account not found"
        );
    }
    
    return $c->render(
        status => 200,
        text => $accountDetails
    );
});

####################     Main   #############################

sub main {

    $username = $ARGV[0];
    my $endpoint = $ARGV[1];

    if (!$username) {
        print "Missing username";
        exit 0;
    }
    
    if (!$endpoint) {
        $endpoint = '/accounts/new';
    }
    
    my $url = Mojo::URL->new($endpoint);
    my $ua = Mojo::UserAgent->new();
    $ua->server->app($app);
    my $response = $ua->get($url);
    print $response->res->content->asset->{'content'};
    $dbh->disconnect();
}

main();
1;

__DATA__

@@ forbidden.html.ep
% layout 'default';
<h1>Forbidden</h1>
<p><%= $content %></p>

@@ unauthorized.html.ep
% layout 'default';
<h1>Unauthorized</h1>
<p><%= $content %></p>

@@ not_found_cust.html.ep
% layout 'default';
<h1>Not found</h1>
<p><%= $content %></p>

@@ not_found.html.ep
% layout 'default';
<h1>Not found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <head><title>MyApp</title></head>
  <body><%= content %></body>
</html>
