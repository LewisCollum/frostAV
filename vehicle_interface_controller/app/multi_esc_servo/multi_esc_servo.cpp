#include <util/delay.h>
#include "dual_servo.hpp"
#include "String.hpp"
#include "usart.hpp"
#include <stdlib.h>

int main() {
    usart::beginAtBaud(9600);
    dual_servo::start();

    uint16_t servoPosition = 1500;
    uint16_t motorPosition = 1500;
    int8_t servoIncrement = 50;
    int8_t motorIncrement = 5;

    //Arduino pin 10. Hooked up to steering servo
    dual_servo::setMicrosB(servoPosition);
    
    //Arduino Pin 9. Hooked up to ESC for motor.
    dual_servo::setMicrosA(motorPosition);
    _delay_ms(2000); //Wait for arming sequence    

	while(1) {
        if (motorPosition >= 1580 || motorPosition <= 1420) motorIncrement = -motorIncrement;
        if (servoPosition >= 1900 || servoPosition <= 1100) servoIncrement = -servoIncrement;

        servoPosition += servoIncrement;
        dual_servo::setMicrosB(servoPosition);
        
        motorPosition += motorIncrement;
        dual_servo::setMicrosA(motorPosition);

        _delay_ms(50);
    }
}
