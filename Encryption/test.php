<?php
// Basic PHP test to ensure mysqli works
error_reporting(E_ALL);
ini_set('display_errors', 1);

$conn = new mysqli("localhost", "root", "Scotland25", "save_contact");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {
    echo "Connection successful!";
}

$conn->close();
?>
<!-- 

<?php
echo "PHP is working!";
?> -->
