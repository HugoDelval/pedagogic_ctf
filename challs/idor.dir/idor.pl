#! /usr/bin/env perl

use strict;
use warnings;
use DBI;
use Mojolicious;
use Mojo::Log;
use Mojo::URL;
use Mojo::UserAgent;
use String::Random qw(random_regex);

my $driver = "SQLite";
my $dsn = "DBI:$driver:dbname=/tmp/idor.db";
my $dbh = DBI->connect($dsn, undef, undef, { AutoCommit => 1 }) or exit;

my $username = "";
my $app = Mojolicious->new;
$app = $app->log(Mojo::Log->new(path => '/dev/null'));


sub generateToken {
    #
    #    Generate a pseudo-random token
    #
    return random_regex("[0-9a-zA-Z]{64}");
}


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

######################   API   ##############################

$app->hook(before_dispatch => sub {
    #
    #    Get token from HTTP header
    #
    my $c = shift;
    my $endpoint = $c->req->url->path;
   
    if ($endpoint eq '/accounts/new'){
        return;
    }
    
    my $token = $c->req->headers->header('X-API-TOKEN');
    my $sth = $dbh->prepare("SELECT username FROM accounts WHERE token=? and username=?");
    $sth->bind_param(1, $token);
    $sth->bind_param(2, $username);
    $sth->execute;
    my $user = $sth->fetchrow_array;
    
    if (!$user) {
        return $c->render(
            status => 401,
            template => 'unauthorized',
            content => 'Invalid X-Api-Token'
         );
    }
});

$app->routes->get('/accounts/new' => sub {
    #
    #    Get account details for user
    #
    my $c = shift;
    my $token = generateToken();
    my $defaultBalance = 100;
    
    my $sth = $dbh->prepare("INSERT OR REPLACE INTO accounts(username, token, balance) VALUES(?,?,?)");
    $sth->bind_param(1, $username);
    $sth->bind_param(2, $token);
    $sth->bind_param(3, $defaultBalance);
    $sth->execute;

    $sth = $dbh->prepare("SELECT id from accounts WHERE username=?");
    $sth->bind_param(1, $username);
    $sth->execute;
    my $accountId = $sth->fetchrow;

    my $response = "Your account $accountId has been successfully created.
    Your associated token is $token
    You can view account details here /accounts/$accountId/details
    ";

    return $c->render(
        status => 200,
        text => $response
    );
});

$app->routes->get('/accounts/(:id)/details' => sub {
    #
    #    Return secret page
    #
    # Username and token already verified in function verify_token
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
    my $token = $ARGV[1];
    my $endpoint = $ARGV[2];

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
    my $response = $ua->get($url => {'X-API-TOKEN' => $token});
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
