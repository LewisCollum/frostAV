#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "usart.hpp"
#include "I2C_slave.hpp"
#include <string.h>


constexpr uint8_t prescaler = 8;
constexpr uint32_t clockFrequency = F_CPU;
constexpr uint8_t pwmFrequency = 50;
constexpr uint32_t baud = 9600;
constexpr uint8_t addr = 0x12;
volatile char* i2cbuffer;
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


static constexpr uint32_t microsToCycles(uint16_t micros) {
    constexpr uint32_t unitConversion = 1E6;
    return (clockFrequency/unitConversion/prescaler) * micros;
}

static constexpr uint32_t hertzToCycles(uint16_t hertz) {
    return clockFrequency/prescaler/hertz;
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
	//if(pidcounter < 100)
	//{
	servoMicros = steeringPid.updateError(error) + servoMicros;
	servoMicros = steeringClamp.clamp(servoMicros);
	OCR1A = ICR1 - microsToCycles(servoMicros);
	
    //String<10> buffer;
	//itoa(servoMicros, buffer, 10); 
    //usart::print(buffer); 
	//buffer.clear();
	//usart::print(", ");
    //itoa(error, buffer, 10); 
    //usart::print(buffer); 
	//usart::print("\r\n");
	
	//error =	50-pidcounter;	//idealServoMicros - servoMicros;
	
	//pidcounter++;
	//}
	TCNT0 = 0x0; //Reset timer count
}

int main() {
	usart::setup(clockFrequency, baud);
    I2C_init(addr);
	setupTimerInterrupt();
    setupServoPwm();
	
	String<10> message;
	int length;

	
	//interrupt enable
	sei();
	
	while(1) {
		i2cbuffer = rxbuffer;
		length = (int)buffer_address;
		if (trigger == true)
		{
			for(int n = 0; n <= length; n++)
			{
				message.append(rxbuffer[n]);
				//rxbuffer[n] = 0;
			}
			//initialServoMicros = atoi(message);
			//servoMicros = steeringClamp.clamp(initialServoMicros);
			//OCR1A = ICR1 - microsToCycles(servoMicros);
			//error = idealServoMicros - servoMicros;
			error = atoi(message);
			usart::print("GOT: ");
            usart::print(message);
            usart::print("\r\n");
			
			//_delay_ms(1000); //remove this, just for testing

			pidcounter = 0;
			
			message.clear();
			trigger = false;
		}
	}
}
