<?php
if($_POST["message"]) {
mail("mail@till-knollmann.com", $_POST["name"],
$_POST["message"]. $_POST("email"));
}
?>