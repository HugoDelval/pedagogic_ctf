#! /usr/bin/env perl

use strict;
use warnings;
use Digest::SHA  qw(sha1_hex);
use MIME::Base64;
use Crypt::CBC;
use Crypt::Cipher::AES;
use Mojolicious;
use Mojo::Log;
use Mojo::URL;
use Mojo::UserAgent;

my $app = Mojolicious->new;
$app = $app->log(Mojo::Log->new(path => '/dev/null'));
my $plain = "";

######################   API   ##############################

$app->routes->get('/encrypted-text' => sub {
    #
    #    Return encrypted text
    #
    my $c = shift;

    # following SOC advisory:
    open my $fh, '<', 'key' or die "error opening key file";
    # 1) Removed plain AES key used to cipher secret from code
    my $secretKey = do { local $/; <$fh> };
    # 2) use an IV that change at every request
    my $iv = encode_base64(time(),'');
    # 3) Use military grade encryption cipher
    eval {
#-literal_key    If true, the key provided by "key" is used directly for encryption/decryption.  Otherwise the actual key used will be a hash of the provided key.  (default false)
      my $cbc = Crypt::CBC->new( -cipher=>'Cipher::AES',-header=>'none', -key=>$secretKey, -iv=>$iv, -padding=>"none", -literal_key=>1, -keysize=>16);
      my $ciphertext = $cbc->encrypt($plain);
      return $c->render(
        status => 200,
        text => "Here is the encrypted text to be pass to your other app: $iv.".encode_base64($ciphertext)
      );
    };
    if ($@) {
      # hum... anyway, crypto should not rely on obscurity!
      return $c->render(
        status => 200,
        text => "Encryption problem!\nIs your message 16 bytes long?\nDumping usefull info:\n $secretKey");
    }
});

####################     Main   #############################

sub main {

    if ($#ARGV < 0) {
      open my $fh, '<', 'secret' or die "error opening secret file";
      $plain = do { local $/; <$fh> };
    }
    else {
      if ($ARGV[0] eq "") {
                open my $fh, '<', 'secret' or die "error opening secret file";
                $plain = do { local $/; <$fh> };
        }
      else { $plain = $ARGV[0]; }
    }

    my $endpoint = '/encrypted-text';

    my $url = Mojo::URL->new($endpoint);
    my $ua = Mojo::UserAgent->new();
    $ua->server->app($app);
    my $response = $ua->get($url);
    print $response->res->content->asset->{'content'};
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
