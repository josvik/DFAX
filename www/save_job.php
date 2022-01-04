<?php

if (ISSET($_POST['save'])) {

  require 'db.php';
  $dbConn = (new DBconn())->getDBconn();
    
  $query = "INSERT INTO jobs (status, script, command, arguments, inputpath, outputpath) VALUES (0, ?, ?, ?, ?, ?)";
  $bindings = [$_POST['script'], $_POST['command'], implode(" ", $_POST['arguments']), $_POST['inputpath'], $_POST['outputpath']];

  if (ISSET($_POST['jobid']) && $_POST['jobid']) {
    $query = "UPDATE jobs SET script=?, command=?, arguments=?, inputpath=?, outputpath=? WHERE jobid=?";
    $bindings[] = $_POST['jobid'];
  }
  echo "<br />Query: ";
  print_r($query);
  echo "<br /> ";
  print_r($bindings);
  echo "<br /> ";
  $stmt = $dbConn->prepare($query);
  $dbResult = $stmt->execute($bindings);

  if (!$dbResult or !$stmt or $stmt->rowCount() == 0) {
    echo "<br/>\nPDO::errorCode():<br/>\n";
    print_r($dbConn->errorCode());
    echo "<br/>\nPDO::errorInfo():<br/>\n";
    print_r($dbConn->errorInfo());
  } else{
    header('location: index.php');
  }
}

?>
