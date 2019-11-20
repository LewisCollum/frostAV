<?php 
  
// Use ls command to shell_exec 
// function 
$output = shell_exec('(sensors | grep curr1)'); //'bash -c 'sensors');// | grep power | sed 's/[^0-9]*//g'''); 

$test = trim($output);
$test = substr($test, -2);

$output = preg_replace('/^[^:]+:\s*/', '' ,$output); 

echo "$unit";

$output = preg_replace('/[^0-9^.]*/', '', $output);

if (strcmp($test, 'mA') !== 0) {
	$num = floatval($output);
	$num = $num*1000;
	$output = strval ($num);
}

//$output2 = preg_replace( '[^0-9]*', '', $output); 
// Display the list of all file 
// and directory 
echo "$output"; 
?> 

