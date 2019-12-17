#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "I2C_slave.hpp"
#include <string.h>

constexpr uint8_t prescaler = 8;
//constexpr uint32_t clockFrequency = F_CPU;
constexpr uint8_t pwmFrequency = 50;
constexpr uint8_t addr = 0x12;

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


static constexpr uint32_t microsToCycles(uint16_t micros) {
    constexpr uint32_t unitConversion = 1E6;
    return (F_CPU/unitConversion/prescaler) * micros;
}

static constexpr uint32_t hertzToCycles(uint16_t hertz) {
    return F_CPU/prescaler/hertz;
}

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
	ICR1 = hertzToCycles(pwmFrequency)-1;
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
	OCR1A = ICR1 - microsToCycles(servoMicros);
	
	TCNT0 = 0x0; //Reset timer count
}

int main() {
    I2C_init(addr);
	setupTimerInterrupt();
    setupServoPwm();
	
	String<10> message;
	int length;

	//interrupt enable
	sei();
	
	while(1) {
		length = (int)buffer_address;
		if (trigger == true)
		{
			for(int n = 0; n <= length; n++)
			{
				message.append(rxbuffer[n]);
			}
			
			error = atoi(message);
			
			message.clear();
			trigger = false;
		}
	}
}
