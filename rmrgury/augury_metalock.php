<?php
  ob_start('ob_gzhandler');
  header('Content-type: application/json');
  include 'config_private.php';
  
  $conn = new mysqli($servername, $username, $password, $dbname);
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }
  mysqli_set_charset($conn, "utf8");
  $sql = "show processlist";
  $result = $conn->query($sql);
  $rows = array();
  while ($row = $result->fetch_assoc()) {
    $rows[] = $row;
  }
  print json_encode($rows);

  $conn->close();
?>
