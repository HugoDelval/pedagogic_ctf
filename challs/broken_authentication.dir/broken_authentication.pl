#! /usr/bin/env perl

use strict;
use warnings;
use DBI;
use Digest::SHA  qw(sha1_hex);
use MIME::Base64;
use Mojolicious;
use Mojo::Log;
use Mojo::URL;
use Mojo::UserAgent;

my $driver = "SQLite";
my $dsn = "DBI:$driver:dbname=/tmp/broken_authentication.db";
my $dbh = DBI->connect($dsn, undef, undef, { sqlite_see_if_its_a_number => 1, AutoCommit => 1 }) or exit;

my $username = "";
my $userTokenMapping = "";
my $app = Mojolicious->new;
$app = $app->log(Mojo::Log->new(path => '/dev/null'));


sub generateUserToken {
    #
    #    Generates an API token for given username
    #
    my $username = shift;
    my $encoded = encode_base64($username, "");
    my $digest = sha1_hex($encoded);
    return $digest;
}

######################   API   ##############################

$app->hook(before_dispatch => sub {
    #
    #    Get token from HTTP header
    #
    my $c = shift;
    my $endpoint = $c->req->url->path;
   
    if ($endpoint eq '/get-token'){
        return;
    }
    
    my $token = $c->req->headers->header('X-API-TOKEN');
    my $sth = $dbh->prepare("SELECT username FROM users WHERE token=?");
    $sth->bind_param(1, $token);
    $sth->execute;
    $userTokenMapping = $sth->fetchrow_array;
    
    if (!$userTokenMapping) {
        return $c->render(
            status => 401,
            template => 'unauthorized',
            content => 'Invalid X-Api-Token'
         );
    }
});

$app->routes->get('/me' => sub {
    #
    #    Returns username based on api token value
    #
    my $c = shift;
    return $c->render(
        status => 200, 
        text => "Your token match the user '$userTokenMapping'"
    );
});

$app->routes->get('/get-token' => sub {
    #
    #    Create or update token for current user
    #
    my $c = shift;

    if ($username eq 'admin') {
        return $c->render(
            status => 403,
            template => 'forbidden',
            content => 'You are not allowed to request token for user admin'
        );
    }
    my $token = generateUserToken($username);
    my $sth = $dbh->prepare("INSERT OR REPLACE INTO users(username, token) VALUES(?, ?)");
    $sth->bind_param(1, $username);
    $sth->bind_param(2, $token);
    $sth->execute;
    
    return $c->render(
        status => 200,
        text => "Your API token is $token"
    );
});

$app->routes->get('/get-secret' => sub {
    #
    #    Return secret page
    #
    my $c = shift;
    if ($userTokenMapping ne 'admin') {
        return $c->render(
            status => 403,
            template => 'forbidden',
            content => "You are not allowed to request /get-secret"
        );
    }
    
    open my $fh, '<', 'secret' or die "error opening secret file";
    my $secret = do { local $/; <$fh> };
    return $c->render(
        status => 200, 
        text => "You are logged in. And congratz ! Here is the secret : $secret"
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
        $endpoint = '/get-token';
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

@@ not_found.html.ep
% layout 'default';
<h1>Not found</h1>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <head><title>MyApp</title></head>
  <body><%= content %></body>
</html>
