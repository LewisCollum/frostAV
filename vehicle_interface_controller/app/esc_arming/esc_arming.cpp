#include <util/delay.h>
#include "car.hpp"
#include "String.hpp"
#include "usart.hpp"
#include <stdlib.h>

int main() {
    usart::beginAtBaud(9600);
    car::start();
    
    car::esc::setMicrosToArm();
    _delay_ms(1000); //Wait for arming sequence

    
    //Use COM tool to send microsecond values to Arduino.
    String<10> message;
    char currentChar;
	while(1) {
        currentChar = usart::getChar();
        
        if (currentChar != '\n') message.append(currentChar);
        else {
            int16_t escMicros = atoi(message);
            car::esc::setMicrosForward(escMicros);
            message.clear();
        }
    }
}
