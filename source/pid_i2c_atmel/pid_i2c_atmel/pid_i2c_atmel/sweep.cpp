#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "usart.hpp"
#include "I2C_slave.hpp"


constexpr uint8_t prescaler = 8;
constexpr uint32_t clockFrequency = F_CPU;
constexpr uint8_t pwmFrequency = 50;
constexpr uint32_t baud = 9600;
constexpr uint8_t addr = 0x12;
char* message;


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

int main() {
	usart::setup(clockFrequency, baud);
    I2C_init(addr);
    setupServoPwm();
    
    Clamp steeringClamp = Clamp::makeFromBounds({
            .lower = 800,
            .upper = 2200 });
    Pid steeringPid = Pid::makeFromScaledGain(10, {
            .proportional = 10,
            .integral = 0,
            .derivative = 0 });

    int16_t idealServoMicros = 1500;
	
	//interrupt enable
	sei();
	
	while(1) {
		message	= (char*)(&rxbuffer);
        int16_t initialServoMicros = atoi(message);
        int16_t servoMicros = steeringClamp.clamp(initialServoMicros);
        OCR1A = ICR1 - microsToCycles(servoMicros);
        _delay_ms(1000);            
            
        int16_t error = idealServoMicros - servoMicros;
        for (uint32_t i = 0; i < 15; ++i) {
			servoMicros = steeringPid.updateError(error) + servoMicros;

			servoMicros = steeringClamp.clamp(servoMicros);
			OCR1A = ICR1 - microsToCycles(servoMicros);
			_delay_ms(100);

			//TODO replace with actual feedback error
			error = idealServoMicros - servoMicros; 
		           
        } 
	}
}
