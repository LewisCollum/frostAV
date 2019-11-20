<?php 
  
// Use ls command to shell_exec 
// function 
$output = shell_exec('(sensors | grep power)'); //'bash -c 'sensors');// | grep power | sed 's/[^0-9]*//g'''); 

$output = preg_replace('/^[^:]+:\s*/', '' ,$output); 

$output = preg_replace('/[^0-9^.]*/', '', $output); 

//$output2 = preg_replace( '[^0-9]*', '', $output); 
// Display the list of all file 
// and directory 
echo "$output"; 
?> 

