<!DOCTYPE html>
<?
# ========================================================
# PHP Web-App for controlling PiBot-A
# Version 1.1 - by Thomas Schoch - www.retas.de
# ========================================================

# Number of spaces placed left of option in dropdown menu
# (emulation of missing "text-align:center" on iPhone)
$spaces = array(
    "oa" => 2,
    "lf" => 7,
    "ms" => 6,
    "rt" => 8,
);

# Call robot.sh, argument is value of pressed button
# or selected operational mode
if (isset ($_POST['mode'])) {
    $mode = $_POST['mode'];
    exec ("sudo /home/pi/robot/robot.sh $mode");
}
if (isset ($_POST['button'])) {
    $action = strtolower ($_POST['button']);
    exec ("sudo /home/pi/robot/robot.sh $action");
}

# Read values needed for the "battery bar" from files
$max  = file_get_contents("/home/pi/sys/runtime.max");
$time = file_get_contents("/home/pi/sys/runtime");
$min  = split(" ", trim($time))[1];

# Calculate status of runtime
$bb_val = intval(100 * ($max - $min) / $max);
$bb_val < 5 && $bb_val = 5;
if ($bb_val >= 30) {
    $bb_stat = "ok";
} elseif ($bb_val >= 10) {
    $bb_stat = "warn";
} else {
    $bb_stat = "low";
}

# Show status of runtime through colors in "battery bar"
$bb_css="class=\"bb-$bb_stat\" style=\"width: $bb_val%\"";

# Read robot.cfg into an array $cfg for dropdown-list
$cfg = file("/home/pi/robot/robot.cfg");
?>

<!-- ===================== HTML ====================== -->
<html>
  <head>
  <link rel="apple-touch-icon-precomposed"
    href="apple-touch-icon-precomposed.png">
  <!-- optimization for iPhone -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style"
    content="black-translucent">
  <meta http-equiv="refresh" content="60">
  <link type="text/css" rel="stylesheet" href="robot.css">
  <title>PiBot-A</title>
  </head>
  <body>
    <center>
    <h1>PiBot-A</h1>
    <h2>Robot</h2>
    <form name="mode" action="#" method="post">
      <select name="mode"
        onChange="document.forms['mode'].submit()">
        <!-- dynamically generated dropdown-list -->
<?
foreach ($cfg as $line) {
  list($state, $mode, $descr) = split(" ", trim($line),3);
  $selected = ($state == "1" ? " selected" : "");
  $nbsp = str_repeat("&nbsp;", $spaces[$mode]);
  $para = "value=\"$mode\"$selected";
  echo "<option $para>$nbsp$descr</option>\n";
}
?>
      </select>
    </form>
    <form name="button" method="post">
      <input type="submit" name="button" value="Start">
      <input type="submit" name="button" value="Stop">
      <h2>System</h2>
      <div class="bb-table">
        <div <?=$bb_css?>></div><div></div>
      </div>
      <input type="submit" name="button" value="Reset">
      <input type="submit" name="button" value="Down">
    </form>
    </center>
  </body>
</html>
