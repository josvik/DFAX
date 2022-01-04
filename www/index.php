<!DOCTYPE html>
<html>
<head>
  <!--<link rel="stylesheet" type="text/css" href="css/bootstrap.css"/>-->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
</head>
<body>
  </br>
  </br>
<!--  <div class="col-md-3"></div>-->
  <div class="col-md-6 well">
    <h3 class="text-primary">DFAX - Digital Forensic Artifact eXtractor</h3>
    <hr style="border-top:1px dotted #ccc;"/>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#jobModal">
      Add job
    </button>
    <div class="modal fade" id="jobModal" tabindex="-1" role="dialog" aria-labelledby="jobModalLongTitle" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <form method="POST" action="save_job.php">
          <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="jobModalLongTitle">Job  </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
            </div>
<?php include 'modal_body.php'; ?>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              <button type="submit" name="save" class="btn btn-primary">Save changes</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    
    <br /><br />
    <table class="table table-bordered">
      <thead class="alert-info">
        <tr>
          <th>JobId</th>
          <th>Script</th>
          <th>Command</th>
          <th>Arguments</th>
          <th>Inputpath</th>
          <th>Outputpath</th>
          <th>Start</th>
          <th>End</th>
        </tr>
      </thead>
      <tbody style="background-color:#fff;">
        <?php
          require 'db.php';
          $dbConn = (new DBconn())->getDBconn();
          $query = $dbConn->prepare("SELECT * FROM `jobs`");
          $query->execute();
          while($fetch = $query->fetch()){
        ?>
        <tr>
          <td><?php echo $fetch['jobid']?></td>
          <td><?php echo $fetch['script']?></td>
          <td><?php echo $fetch['command']?></td>
          <td><?php echo $fetch['arguments']?></td>
          <td><?php echo $fetch['inputpath']?></td>
          <td><?php echo $fetch['outputpath']?></td>
          <td><?php echo $fetch['start']?></td>
          <td><?php echo $fetch['end']?></td>
        </tr>
        <?php
          }
          $dbConn = null;
        ?>
      </tbody>
    </table>
  </div>
  
<!--<script src="js/jquery-3.6.0.min.js"></script>-->
<!--<script src="js/bootstrap.js"></script>-->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
