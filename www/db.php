<?php
class DBconn {
  private $dbConn;
  
  public function getDBconn() {
    if ($this->dbConn == null) {
      // Remember to give the www-user write-permissions to the db file.
      $this->dbConn = new PDO("sqlite:".__DIR__."/../db/dfax.db");
      $query = "CREATE TABLE IF NOT EXISTS 'jobs' ('jobid' INTEGER UNIQUE, 'status' INT DEFAULT 0, 'script' TEXT, 'command' TEXT, 'arguments' TEXT, 'inputpath' TEXT, 'outputpath' TEXT, 'start' DATETIME, 'end' DATETIME,PRIMARY KEY('jobid' AUTOINCREMENT))";
      
      $this->dbConn->exec($query);
    }
    return $this->dbConn;
  }
}
?>
