#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "usart.hpp"
#include "dual_servo.hpp"

int main() {
    int16_t idealServoMicros = 1500;
    
    usart::beginAtBaud(9600);
    dual_servo::start();
    dual_servo::setMicrosA(idealServoMicros);    

    Clamp steeringClamp = Clamp::makeFromBounds({
            .lower = 800,
            .upper = 2200 });
    Pid steeringPid = Pid::makeFromScaledGain(10, {
            .proportional = 10,
            .integral = 0,
            .derivative = 0 });
    
    String<10> message;
    char currentChar;
	while(1) {
        currentChar = usart::getChar();
        
        if (currentChar != '\n') message.append(currentChar);
        else {
            int16_t initialServoMicros = atoi(message);
            int16_t servoMicros = steeringClamp.clamp(initialServoMicros);
            dual_servo::setMicrosA(servoMicros);
            _delay_ms(1000);            

            //Pid loop
            int16_t error = idealServoMicros - servoMicros;
            for (uint32_t i = 0; i < 15; ++i) {
                servoMicros = steeringPid.updateError(error) + servoMicros;

                String<10> buffer;
                itoa(servoMicros, buffer, 10); 
                usart::print(buffer); usart::print('\n');

                servoMicros = steeringClamp.clamp(servoMicros);
                dual_servo::setMicrosA(servoMicros);
                _delay_ms(100);

                //TODO replace with actual feedback error
                error = idealServoMicros - servoMicros;
            }
            
            message.clear();
            usart::print("\n>> ");
        } 
	}
}
