#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "usart.hpp"
#include "Cycles.hpp"

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

	ICR1 = Cycles::fromHertz(50)-1;
}

int main() {
    Cycles::prescaler = 8;
    usart::beginAtBaud(9600);
    setupServoPwm();
    
    Clamp steeringClamp = Clamp::makeFromBounds({
            .lower = 800,
            .upper = 2200 });
    Pid steeringPid = Pid::makeFromScaledGain(10, {
            .proportional = 10,
            .integral = 0,
            .derivative = 0 });
    
    String<10> message;
    char currentChar;
    int16_t idealServoMicros = 1500;
	while(1) {
        currentChar = usart::getChar();
        
        if (currentChar != '\n') message.append(currentChar);
        else {
            usart::print("GOT: ");
            usart::print(message);
            usart::print('\n');
            
            int16_t initialServoMicros = atoi(message);
            int16_t servoMicros = steeringClamp.clamp(initialServoMicros);
            OCR1A = ICR1 - Cycles::fromMicros(servoMicros);
            _delay_ms(1000);            
            
            int16_t error = idealServoMicros - servoMicros;
            for (uint32_t i = 0; i < 15; ++i) {
                servoMicros = steeringPid.updateError(error) + servoMicros;

                String<10> buffer;
                itoa(servoMicros, buffer, 10); 
                usart::print(buffer); usart::print('\n');

                servoMicros = steeringClamp.clamp(servoMicros);
                OCR1A = ICR1 - Cycles::fromMicros(servoMicros);
                _delay_ms(100);

                //TODO replace with actual feedback error
                error = idealServoMicros - servoMicros;
            }
            
            message.clear();
            usart::print(">> ");
        } 
	}
}
