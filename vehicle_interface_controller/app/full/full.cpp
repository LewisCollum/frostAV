#include <avr/io.h>
#include "String.hpp"
#include "usart.hpp"
#include <stdint.h>
#include "car.hpp"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "usart.hpp"
#include "twi.hpp"
#include <avr/interrupt.h>

constexpr uint16_t bufferCapacity = 10;
constexpr Bounds<uint16_t> steeringAngleBounds = {50, 130};
Clamp steeringClamper = Clamp<uint16_t>::makeFromBounds(steeringAngleBounds);

void handler(uint8_t* rxbuffer, int twi_txBufferIndex);

void stateChange(String<bufferCapacity> state) {
    if (state == "+stop")
        car::stop();
}

int main() {
	twi_init();
	twi_attachSlaveRxEvent(handler);
	twi_setAddress(0x32);

    usart::beginAtBaud(9600);
    usart::print("RUNNING");
    car::start();
    
    sei();
 
	while(1) {}
}

void handler(uint8_t* rxbuffer, int twi_txBufferIndex) {
    char* message = reinterpret_cast<char*>(rxbuffer);
    //usart::print(message);
    if (message[0] == '+') stateChange(message);
    else if (isdigit(message[0])) {
        uint16_t steeringAngle = atoi(message);
        uint16_t micros = steeringClamper.mirrorMapValueToBounds(steeringAngle, car::servo::microsBounds);
        
        char steeringMessage[10];
        itoa(micros, steeringMessage, 10);
        usart::print(message);
        usart::print(", ");
        usart::print(steeringMessage);
        usart::print("\n");
        car::servo::setMicros(micros);
        //car::servo::setMirroredPositionFromBounds(steeringAngle, steeringAngleBounds);
        //car::esc::setMicrosForward(car::esc::upperBoundMicros-10);
    }
}
