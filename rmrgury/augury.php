<?php
  ob_start('ob_gzhandler');
  header('Content-type: application/json');
  include 'config_private.php';
  
  $conn = new mysqli($servername, $username, $password, $dbname);
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }
  mysqli_set_charset($conn, "utf8");
  
  function fetch_operations($operation) {
    global $conn;
    if ($operation != 0) {
      $sql = "SELECT t2.idx, opnumber, datetime, year, type, subtype, synopsis, UTM
      FROM operation t2
      LEFT JOIN victimInfo
      ON t2.idx=victimInfo.operationIdx
      WHERE t2.year=" . $operation . "
      GROUP BY t2.idx, opnumber, datetime, year, type, subtype, synopsis, UTM";
    }
    else {
      $sql = "SELECT t2.idx, opnumber, datetime, year, type, subtype, synopsis, UTM
      FROM operation t2
      LEFT JOIN victimInfo
      ON t2.idx=victimInfo.operationIdx
      GROUP BY t2.idx, opnumber, datetime, year, type, subtype, synopsis, UTM";
    }
    $result = $conn->query($sql);
    $rows = array();
    while ($row = $result->fetch_assoc()) {
      $rows[] = $row;
    }
    print json_encode($rows);
  }
  
  function fetch_memberidx($memberidx) {
    global $conn;
    $memberidx = $conn->real_escape_string($memberidx);
    $sql = "SELECT ShortName, privileges, idx FROM member t1 WHERE t1.unixID='" . $memberidx . "'";
    $result = $conn->query($sql);
    $row = $result->fetch_assoc();
    print json_encode($row);
  }
  
  function fetch_missions($missionidx) {
    global $conn;
    $sql = "SELECT operationIdx, t3.datetime, t3.hours, t3.period, t4.function, t4.emergency FROM operation t2, operationalPeriod t3, opattendance t4
      WHERE t2.idx=t3.operationIdx AND t3.idx=t4.opPeriodIdx AND t4.memberIdx=" . $missionidx;
    $result = $conn->query($sql);
    $rows = array();
    while ($row = $result->fetch_assoc()) {
      $rows[] = $row;
    }
    print json_encode($rows);
  }

  function fetch_oos($oosdays) {
    global $conn;
    $rows = array();
    for ($day = -1; $day <= $oosdays; $day++) {
      $sql = "SELECT DATE_FORMAT(date, '%Y-%m-%d') as date, status, COUNT(status) as sum FROM OOS WHERE DATE(date) = DATE_ADD(CURDATE(), INTERVAL " . $day . " DAY) GROUP by status";
      $result = $conn->query($sql);
      while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
      }
    }
    print json_encode($rows);
  }

  function fetch_oos_full($oosdays) {
    global $conn;
    $rows = array();
    $sql = "SELECT DATE_FORMAT(date, '%Y-%m-%d') as date, status, member.FirstName, member.LastName, memberlevel.srank FROM OOS os JOIN member ON member.idx=os.memberIdx JOIN memberlevel ON member.currentRankIdx=memberlevel.idx WHERE DATE(date) >= DATE_ADD(CURDATE(), INTERVAL -1 DAY) AND DATE(date) < DATE_ADD(CURDATE(), INTERVAL " . $oosdays . " DAY)";
      $result = $conn->query($sql);
      while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
      }
    print json_encode($rows);
  }

  function fetch_memberoos($oosdays, $idx) {
    global $conn;
    $rows = array();
    $sql = "SELECT DATE_FORMAT(date, '%Y-%m-%d') as date, status FROM OOS WHERE DATE(date) >= '" . $oosdays . "' AND memberIdx = " . $idx;
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
      $rows[] = $row;
    }
    print json_encode($rows);
  }
  
  function fetch_calltaker($oosdays) {
    global $conn;
    $rows = array();
    $start = 0;
    if ($oosdays > 20) {
      // For updating the schedule, get the whole current week
      $start = -6;
    }
    for ($day = $start; $day <= $oosdays; $day++) {
      $sql = "    SELECT schedentry.idx, startTS, endTS, member.LastName, member.ShortName FROM schedentry
        CROSS JOIN member ON member.idx=schedentry.memberidx
        WHERE DATE(startTS) = DATE_ADD(CURDATE(), INTERVAL " . $day . " DAY) AND fscheduleIdx = 1";
      $result = $conn->query($sql);
      while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
      }
    }
    print json_encode($rows);
  }

  function fetch_coordinator() {
    global $conn;
    $rows = array();
    $sql = "SELECT schedentry.idx, startTS, endTS, member.LastName, member.ShortName FROM schedentry
      CROSS JOIN member ON member.idx=schedentry.memberidx
      WHERE DATE(startTS) >= '2024-01-01' AND fscheduleIdx = 2";
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
      $rows[] = $row;
    }
    print json_encode($rows);
  }

  function fetch_callmember($callmember) {
    global $conn;
    $memberidx = $conn->real_escape_string($memberidx);
    $sql = "SELECT ShortName, LastName, FirstName, privileges, idx FROM member t1 WHERE privileges like '%Call Taker%'";
    $result = $conn->query($sql);
    $rows = array();
    while ($row = $result->fetch_assoc()) {
      $rows[] = $row;
    }
    print json_encode($rows);
  }
  
  function handle_get() {
    $operation = filter_input(INPUT_GET,"operations",FILTER_SANITIZE_NUMBER_INT);
    $memberidx = filter_input(INPUT_GET,"memberidx",FILTER_SANITIZE_ENCODED);
    $missionidx = filter_input(INPUT_GET,"missionidx",FILTER_SANITIZE_NUMBER_INT);
    $oos = filter_input(INPUT_GET,"oos",FILTER_SANITIZE_NUMBER_INT);
    $oosfull = filter_input(INPUT_GET,"oosfull",FILTER_SANITIZE_NUMBER_INT);
    $oos_single = filter_input(INPUT_GET,"memberoos",FILTER_SANITIZE_ENCODED);
    $call = filter_input(INPUT_GET,"calltaker",FILTER_SANITIZE_NUMBER_INT);
    $coord = filter_input(INPUT_GET,"coordinator",FILTER_SANITIZE_NUMBER_INT);
    $callmember = filter_input(INPUT_GET,"callmember",FILTER_SANITIZE_NUMBER_INT);
    if ($operation !== null) {
      fetch_operations($operation);
    } elseif ($missionidx !== null) {
      fetch_missions($missionidx);
    } elseif ($oosfull !== null) {
      fetch_oos_full($oosfull);
    } elseif ($oos !== null) {
      fetch_oos($oos);
    } elseif ($oos_single !== null && $memberidx != null) {
      fetch_memberoos($oos_single, $memberidx);
    } elseif ($call !== null) {
      fetch_calltaker($call);
    } elseif ($coord !== null) {
      fetch_coordinator($coord);
    } elseif ($memberidx !== null) {
      fetch_memberidx($memberidx);
    } elseif ($callmember !== null) {
      fetch_callmember($callmember);
    } else {
      print('{"result": "unknown request"}');
    }
  }

  function handle_put_oos($json) {
    global $conn;
    $rows = $json->oos;
    $memberidx = $json->memberidx;
    if ($memberidx == null || $memberidx == "") {
      return;
    }
    $result=false;
    foreach($rows as $avail) {
      $status = $avail->status;
      $date = $avail->date;
      $insert = $avail->insert;
      if ($date == null || $status == null) {
        continue;
      }
      if ($status == "Practice") {
        $status = "At Practice";
      }
      if ($insert != null && $insert == "1") {
        $sql = "INSERT INTO OOS (status, date, memberIdx) VALUES ( '" . $status . "', '" . $date . "', " . $memberidx . ");";
      } else {
        $sql = "UPDATE OOS SET status='" . $status . "' WHERE date='" . $date . "' AND memberIdx=". $memberidx;
      }
      $result = $conn->query($sql);
    }
    $putresult = ($result) ? "success" : "failed";
    print($putresult);
    //print('{"result": "' . $putresult . '"}');
  }

  function handle_put_call($json) {
    global $conn;
    $rows = $json->calltaker;
    $result=false;
    $records=0;
    foreach($rows as $avail) {
      $index = $avail->index;
      $start = $avail->startDate;
      $finish = $avail->endDate;
      $action = $avail->action;
      $memberIdx = $avail->memberIdx;
      if ($records > 10) {
        // Failsafe in case we have some crazy or malicious json
        break;
      }
      $records=$records+1;
      if (empty($start) || empty($finish) || empty($index) || empty($action) || empty($memberIdx)) {
        continue;
      }
      if ($index < 0 && $action != "add" ) {
        continue;
      }
      if ($action == "add") {
        $sql = "INSERT INTO schedentry (memberIdx, fscheduleIdx, startTS, endTS) VALUES ( " . $memberIdx . ", 1,  '" . $start . "', '" . $finish . "');";
      } elseif ($action == "delete") {
        $sql = "DELETE FROM schedentry WHERE idx=". $index;
      } else {
        $sql = "UPDATE schedentry SET memberIdx=" . $memberIdx . ", startTS='" . $start . "', endTS='" . $finish . "' WHERE idx=". $index;
      }
      $result = $conn->query($sql);
    }
    $putresult = ($result) ? "success" : "failed";
    print('{"result": "' . $putresult . '", "error": "' . mysqli_error($conn) . '"}');
  }

  function handle_put($json) {
    if ($json->request == "oos") {
      handle_put_oos($json);
    } elseif ($json->request == "call") {
      handle_put_call($json);
    } else {
      print('{"result": "unknown request"}');
    }
  }
  
  // Main
  $method = $_SERVER['REQUEST_METHOD'];
  if ('PUT' === $method) {
    $putinput = file_get_contents('php://input');
    $json = json_decode($putinput);
    handle_put($json);
  } else {
    handle_get();
  }

  $conn->close();
?>
