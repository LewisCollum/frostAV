EESchema Schematic File Version 4
LIBS:Senior Design Power PCB-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Analog_ADC:INA226 U1
U 1 1 5D7A9EC1
P 3750 3700
F 0 "U1" H 3750 4450 50  0000 C CNN
F 1 "INA226" H 3750 4350 50  0000 C CNN
F 2 "Package_SO:VSSOP-10_3x3mm_P0.5mm" H 4550 3250 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/ina226.pdf" H 4100 3600 50  0001 C CNN
	1    3750 3700
	1    0    0    -1  
$EndComp
$Comp
L Regulator_Switching:LM2596S-5 U2
U 1 1 5D7AA788
P 6250 3500
F 0 "U2" H 5950 3850 50  0000 C CNN
F 1 "LM2596SX-5" H 6350 3850 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:TO-263-5_TabPin3" H 6300 3250 50  0001 L CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm2596.pdf" H 6250 3500 50  0001 C CNN
	1    6250 3500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5D7ADEB7
P 3750 4400
F 0 "#PWR0101" H 3750 4150 50  0001 C CNN
F 1 "GND" H 3755 4227 50  0000 C CNN
F 2 "" H 3750 4400 50  0001 C CNN
F 3 "" H 3750 4400 50  0001 C CNN
	1    3750 4400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5D7AE40E
P 6250 4350
F 0 "#PWR0102" H 6250 4100 50  0001 C CNN
F 1 "GND" H 6255 4177 50  0000 C CNN
F 2 "" H 6250 4350 50  0001 C CNN
F 3 "" H 6250 4350 50  0001 C CNN
	1    6250 4350
	1    0    0    -1  
$EndComp
$Comp
L pspice:INDUCTOR L1
U 1 1 5D7AF5DA
P 7200 3600
F 0 "L1" H 7200 3700 50  0000 C CNN
F 1 "33 uH" H 7200 3550 50  0000 C CNN
F 2 "" H 7200 3600 50  0001 C CNN
F 3 "~" H 7200 3600 50  0001 C CNN
	1    7200 3600
	1    0    0    -1  
$EndComp
$Comp
L Diode:1N5822 D1
U 1 1 5D7AFE6C
P 6800 3800
F 0 "D1" V 6754 3879 50  0000 L CNN
F 1 "50WQ04FN" V 6845 3879 50  0000 L CNN
F 2 "Diode_THT:D_DO-201AD_P15.24mm_Horizontal" H 6800 3625 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88526/1n5820.pdf" H 6800 3800 50  0001 C CNN
	1    6800 3800
	0    1    1    0   
$EndComp
Wire Wire Line
	5750 3600 5650 3600
Wire Wire Line
	5650 4050 6250 4050
Wire Wire Line
	6750 3600 6800 3600
Wire Wire Line
	7450 3600 7550 3600
Wire Wire Line
	6800 4050 6250 4050
Connection ~ 6250 4050
Wire Wire Line
	6250 4050 6250 4350
Connection ~ 6800 3600
Wire Wire Line
	6800 3600 6950 3600
Wire Wire Line
	6800 3600 6800 3650
Wire Wire Line
	6800 3750 6800 3800
Wire Wire Line
	6250 3800 6250 4050
$Comp
L Device:CP1 C2
U 1 1 5D7B82A7
P 7550 3850
F 0 "C2" H 7500 3600 50  0000 L CNN
F 1 "680uF 35v (Panasonic FK)" H 7050 3500 50  0000 L CNN
F 2 "" H 7550 3850 50  0001 C CNN
F 3 "~" H 7550 3850 50  0001 C CNN
	1    7550 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7550 3700 7550 3600
Connection ~ 7550 3600
Wire Wire Line
	7550 4000 7550 4050
Wire Wire Line
	7550 4050 6800 4050
Connection ~ 6800 4050
Wire Wire Line
	5350 4000 5350 4050
Wire Wire Line
	5350 4050 5650 4050
Connection ~ 5650 4050
Wire Wire Line
	5650 3600 5650 4050
Wire Wire Line
	5750 3400 5350 3400
Wire Wire Line
	5350 3400 5350 3700
Wire Wire Line
	3750 4200 3750 4250
Wire Wire Line
	4150 3400 4200 3400
Wire Wire Line
	4200 3400 4200 3500
Wire Wire Line
	4200 3500 4150 3500
Wire Wire Line
	4200 3500 4200 4250
Wire Wire Line
	4200 4250 3750 4250
Connection ~ 4200 3500
Connection ~ 3750 4250
Wire Wire Line
	3750 4250 3750 4400
Wire Wire Line
	7550 3100 7550 3400
Wire Wire Line
	3750 3100 3750 3200
Connection ~ 3750 3200
Wire Wire Line
	3750 3200 3750 3250
Connection ~ 7550 3400
$Comp
L Device:R_US RSense
U 1 1 5D7C461B
P 2900 3700
F 0 "RSense" H 2800 3450 50  0000 L CNN
F 1 "0.002 Ohm" H 2750 3350 50  0000 L CNN
F 2 "" V 2940 3690 50  0001 C CNN
F 3 "~" H 2900 3700 50  0001 C CNN
	1    2900 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 3800 3200 3800
Wire Wire Line
	3200 3800 3200 3450
Wire Wire Line
	3200 3450 2900 3450
Wire Wire Line
	3350 3900 3250 3900
Wire Wire Line
	2900 3900 2900 3850
Wire Wire Line
	3350 3400 3250 3400
Wire Wire Line
	3250 3400 3250 3900
Connection ~ 3250 3900
Wire Wire Line
	3250 3900 2900 3900
Wire Wire Line
	3250 3900 3250 4350
Connection ~ 5350 3400
Text GLabel 8150 3400 2    50   Input ~ 0
5V
Wire Wire Line
	8150 3400 7550 3400
Text GLabel 8150 3700 2    50   Input ~ 0
GND
Text GLabel 8150 3100 2    50   Input ~ 0
SDA
Text GLabel 8150 3250 2    50   Input ~ 0
SCL
$Comp
L power:GND #PWR0103
U 1 1 5D7D0F22
P 8100 3950
F 0 "#PWR0103" H 8100 3700 50  0001 C CNN
F 1 "GND" H 8105 3777 50  0000 C CNN
F 2 "" H 8100 3950 50  0001 C CNN
F 3 "" H 8100 3950 50  0001 C CNN
	1    8100 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	8150 3700 8100 3700
Wire Wire Line
	8100 3700 8100 3950
$Comp
L Device:R_US R1
U 1 1 5D7D26E6
P 4350 3450
F 0 "R1" H 4418 3496 50  0000 L CNN
F 1 "4.7K" H 4418 3405 50  0000 L CNN
F 2 "" V 4390 3440 50  0001 C CNN
F 3 "~" H 4350 3450 50  0001 C CNN
	1    4350 3450
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R2
U 1 1 5D7D2C5D
P 4700 3450
F 0 "R2" H 4768 3496 50  0000 L CNN
F 1 "4.7K" H 4768 3405 50  0000 L CNN
F 2 "" V 4740 3440 50  0001 C CNN
F 3 "~" H 4700 3450 50  0001 C CNN
	1    4700 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 3300 4700 3100
Wire Wire Line
	4350 3300 4350 3100
Connection ~ 4350 3100
Wire Wire Line
	4350 3600 4350 3700
Wire Wire Line
	4350 3700 4150 3700
Wire Wire Line
	4700 3800 4700 3600
Wire Wire Line
	5050 4350 5050 3400
Wire Wire Line
	5050 3400 5350 3400
Wire Wire Line
	4150 3800 4700 3800
Wire Wire Line
	4350 3100 4550 3100
Connection ~ 4700 3100
Wire Wire Line
	4700 3100 7550 3100
Wire Wire Line
	4350 3700 4950 3700
Wire Wire Line
	4950 3700 4950 3200
Connection ~ 4350 3700
Wire Wire Line
	4850 3800 4700 3800
Connection ~ 4700 3800
Text GLabel 2500 3450 0    50   Input ~ 0
B+
Text GLabel 2500 3650 0    50   Input ~ 0
B-
Wire Wire Line
	2500 3450 2900 3450
Connection ~ 2900 3450
$Comp
L power:GND #PWR0104
U 1 1 5D7ED7B9
P 2600 4000
F 0 "#PWR0104" H 2600 3750 50  0001 C CNN
F 1 "GND" H 2605 3827 50  0000 C CNN
F 2 "" H 2600 4000 50  0001 C CNN
F 3 "" H 2600 4000 50  0001 C CNN
	1    2600 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2500 3650 2600 3650
Wire Wire Line
	2600 3650 2600 4000
Wire Wire Line
	2900 3450 2900 3550
$Comp
L Device:C C3
U 1 1 5DB20504
P 4550 4050
F 0 "C3" H 4665 4096 50  0000 L CNN
F 1 "0.1 uF" H 4665 4005 50  0000 L CNN
F 2 "" H 4588 3900 50  0001 C CNN
F 3 "~" H 4550 4050 50  0001 C CNN
	1    4550 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3900 4550 3100
Connection ~ 4550 3100
Wire Wire Line
	4550 3100 4700 3100
$Comp
L Device:CP1 C1
U 1 1 5D7B7A85
P 5350 3850
F 0 "C1" H 5300 3600 50  0000 L CNN
F 1 "680uF 35v (Panasonic FK)" H 5100 3500 50  0000 L CNN
F 2 "" H 5350 3850 50  0001 C CNN
F 3 "~" H 5350 3850 50  0001 C CNN
	1    5350 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 4050 6800 3950
Wire Wire Line
	4850 3250 4850 3800
Wire Wire Line
	6750 3400 7550 3400
Wire Wire Line
	7550 3400 7550 3600
Wire Wire Line
	4250 3100 4350 3100
Wire Wire Line
	3750 3100 4350 3100
Wire Wire Line
	8150 3250 4850 3250
Wire Wire Line
	8150 3100 7950 3100
Wire Wire Line
	7950 3100 7950 3200
Wire Wire Line
	7950 3200 4950 3200
Wire Wire Line
	3250 4350 5050 4350
Wire Wire Line
	4550 4200 4550 4250
Wire Wire Line
	4550 4250 4200 4250
Connection ~ 4200 4250
$EndSCHEMATC
