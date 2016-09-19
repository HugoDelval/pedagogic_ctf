#!/usr/bin/php
<?php
header('Content-type: text/html; charset=utf-8');
$mail= $argv[1];


 
if (filter_var($mail, FILTER_VALIDATE_EMAIL))
{
    generate_config($mail);
}
else
{
    echo 'Bad mail adress format.';
}
 
function generate_config ($mail)
{
$text="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>EmailAccountDescription</key>
            <string>$mail</string>
            <key>EmailAccountType</key>
            <string>EmailTypeIMAP</string>
        </dict>
    </array>
    <key>PayloadDescription</key>
    <string>By installing this profile your email account will be automatically added to your iPhone, removing the need for manual configuration.</string>
    <key>PayloadDisplayName</key>
    <string>Autoconfig-$mail</string>
    <key>PayloadIdentifier</key>
    <string>Autoconfig-$mail</string>
    <key>PayloadOrganization</key>
    <string>Autoconfig-$mail</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>c385172c-f659-11e5-803a-60a44c606bab</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>";
$tmpfname = tempnam("/tmp", "$mail.mobileconfig");
$tmpfname2=tempnam("/tmp", "$mail.signed.mobileconfig");
$ser_crt="autoconfig-email.crt";
$ser_key="autoconfig-email.key";
$chain="chain.crt";
$pass="pwgen";
$handle = fopen($tmpfname, "w") ;
if (!handle)
{
    die ("Can't open file");
}
 
if (!fwrite($handle, $text))
{
    die ("Unable to create the config file");
}
 
if (!fclose($handle))
{
    die ("There is a problem to closing file.");
}
echo "openssl smime -sign -in $tmpfname -out $tmpfname2 -signer $ser_crt -inkey $ser_key -certfile $chain -outform der -nodetach -passin pass:$pass";
if (system ("openssl smime -sign -in $tmpfname -out $tmpfname2 -signer $ser_crt -inkey $ser_key -certfile $chain -outform der -nodetach -passin pass:$pass"))
{
    die ("Can't generate crypted file");
}
$file=$tmpfname2;
$fichier_taille = filesize($file);
header('Content-type: application/x-apple-aspen-config; chatset=utf-8');
header("Content-disposition: attachment; filename=$mail.signed.mobileconfig");
readfile($file);
sleep (2);
if (!unlink ($tmpfname))
{
    die ("There is a problem to delete tmp file");
}
if (!unlink ($tmpfname2))
{
    die ("There is a problem to delete tmp file");
}
}
 
?>
