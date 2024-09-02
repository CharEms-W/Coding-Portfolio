<?php
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

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO contacts (first_name, last_name, message) VALUES (?, ?, ?)");
$stmt->bind_param("sss", $first_name, $last_name, $message);

// Execute the query
if ($stmt->execute()) {
    header('Location: thankyou.html');
} else {
    echo "Error: " . $stmt->error;
}

// Close connection
$stmt->close();
$conn->close();
?>
