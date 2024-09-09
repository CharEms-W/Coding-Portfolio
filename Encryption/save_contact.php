<?php
// Enable error reporting for better debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// MySQL database credentials
$servername = "127.0.0.1";  
$username = "root";  
$password = "Scotland25";  
$dbname = "save_contact";  

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input
    $first_name = htmlspecialchars(strip_tags(trim($_POST['first_name'])));
    $last_name = htmlspecialchars(strip_tags(trim($_POST['last_name'])));
    $message = htmlspecialchars(strip_tags(trim($_POST['message'])));

    // Prepare SQL statement
    $stmt = $conn->prepare("INSERT INTO contacts (first_name, last_name, message) VALUES (?, ?, ?)");
    if ($stmt === false) {
        die("Error in prepare statement: " . $conn->error);
    }

    // Bind parameters
    $stmt->bind_param("sss", $first_name, $last_name, $message);

    // Execute the statement
    if ($stmt->execute()) {
        header('Location: thankyou.html');
        exit();
    } else {
        echo "Error executing statement: " . $stmt->error;
    }

    // Close the statement
    $stmt->close();
}

// Close the database connection
$conn->close();
?>







<!-- <?php

error_reporting(E_ALL);
ini_set('display_errors', 1);


// MySQL database credentials
$servername = "localhost";  // Usually "localhost"
$username = "root";  // MySQL username
$password = "Scotland25";  // MySQL password
$dbname = "save_contact";  // MySQL database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get form data
$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$message = $_POST['message'];

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data and sanitize inputs
    $first_name = htmlspecialchars(strip_tags(trim($_POST['first_name'])));
    $last_name = htmlspecialchars(strip_tags(trim($_POST['last_name'])));
    $message = htmlspecialchars(strip_tags(trim($_POST['message']) ));
}
// Prepare and bind
$stmt = $conn->prepare("INSERT INTO contacts (first_name, last_name, message) VALUES (?, ?, ?)");
$stmt->bind_param("sss", $first_name, $last_name, $message);

// Execute the query
if ($stmt->execute()) {
    header('Location: thankyou.html');
} else {
    echo "Error: " . $stmt->error;
}

// Close the statement
$stmt->close();


// Close connection
$conn->close();

?> -->