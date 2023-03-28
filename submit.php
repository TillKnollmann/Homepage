<?php
if ($_POST["message"]) {
$retval = mail("mail@till-knollmann.com", $_POST["name"], $_POST["message"], "From:" . $_POST["email"] . "\r\n");
if( $retval == true ) {
    echo "Sent";
 }else {
    echo "Failed";
 }
}
