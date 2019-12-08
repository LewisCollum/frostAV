#include <util/delay.h>
#include "String.hpp"
#include "usart.hpp"
#include <stdlib.h>
#include "car.hpp"

int main() {
    usart::beginAtBaud(9600);
    car::start();

    uint16_t servoPosition = 1500;
    uint16_t motorPosition = 1500;
    int8_t servoIncrement = 50;
    int8_t motorIncrement = 5;

	while(1) {
        if (motorPosition >= 1580 || motorPosition <= 1420) motorIncrement = -motorIncrement;
        if (servoPosition >= 1900 || servoPosition <= 1100) servoIncrement = -servoIncrement;

        servoPosition += servoIncrement;
        car::servo::setMicros(servoPosition);
        
        motorPosition += motorIncrement;
        car::esc::setMicros(motorPosition);

        _delay_ms(50);
    }
}
