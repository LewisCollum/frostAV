#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "I2C_slave.hpp"
#include <string.h>
#include "cycles.hpp"


int pidcounter = 15;
int16_t initialServoMicros;
int16_t servoMicros;

Clamp steeringClamp = Clamp::makeFromBounds({
	.lower = 800,
	.upper = 2200 });
Pid steeringPid = Pid::makeFromScaledGain(10, {
	.proportional = 10,
	.integral = 0,
	.derivative = 0 });
	
int16_t idealServoMicros = 1500;
int16_t error;

static void setupServoPwm() {
	DDRB |= 1 << PINB1; //Set pin 9 on arduino to output

	TCCR1A |=
        1 << WGM11 | //PWM Mode 14 (1/3)
        1 << COM1A0 | //Inverting Mode (1/2)
        1 << COM1A1; //Inverting Mode (2/2)
    
	TCCR1B |=
        1 << WGM12 | //PWM Mode 14 (2/3)
        1 << WGM13 | //PWM Mode 14 (3/3)
        1 << CS11; //Prescaler: 8

    //50Hz PWM to cycles for servo
	ICR1 = cycles::fromHertz(50)-1;
}

static void setupTimerInterrupt(){
	TCCR0A = 0x00;	
	TCCR0B |= 1 << CS02; //Prescaler: 256 (from 16 mhz)
	OCR0B = (0x30324);	//Trigger every 200 ms (count b)
	TIMSK0 = (1 << OCIE0B); //Interrupt on count B
}

ISR(TIMER0_COMPB_vect)
{ 
	servoMicros = steeringPid.updateError(error) + servoMicros;
	servoMicros = steeringClamp.clamp(servoMicros);
	OCR1A = ICR1 - cycles::fromMicros(servoMicros);
	
	TCNT0 = 0x0; //Reset timer count
}

int main() {
    I2C_init(0x01);
	setupTimerInterrupt();
    setupServoPwm();
	
	String<10> message;
	int length;

	//interrupt enable
	sei();
	
	while(1) {
		length = (int)buffer_address;
		if (trigger == true) {
			for(int n = 0; n <= length; n++) {
				message.append(rxbuffer[n]);
			}

			error = atoi(message);
			pidcounter = 0;
			message.clear();
			trigger = false;
		}
	}
}
