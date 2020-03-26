#include <avr/io.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <avr/interrupt.h>

#include "String.hpp"
#include "car.hpp"
#include "twi.hpp"
#include "usart.hpp"


constexpr uint16_t bufferCapacity = 5; //Must be larger than length of spliced value from message + 1 for null
constexpr uint16_t messageSpliceCount = 3; //The number of data values are we reading.
constexpr uint16_t steeringResolution = 11; //Must be odd to ensure the servo can center
constexpr uint16_t throttleResolution = 21; //Must be odd


constexpr Bounds<car::MicrosType> steeringAngleBounds = {0, steeringResolution-1};
Clamp steeringClamper = Clamp<car::MicrosType>::makeFromBounds(steeringAngleBounds);

constexpr Bounds<car::MicrosType> throttleBounds = {0, throttleResolution-1};
Clamp throttleClamper = Clamp<car::MicrosType>::makeFromBounds(throttleBounds);


void handler(uint8_t * rxbuffer, int twi_txBufferIndex);

int main() {
	twi_init();
	twi_attachSlaveRxEvent(handler);
	twi_setAddress(0x32);

    usart::beginAtBaud(9600);
    usart::print("Started\n");

    car::start();
    
    sei();
    
	while(1) {}
}

void handler(uint8_t * rxbuffer, int twi_txBufferIndex) {
    char * message = reinterpret_cast<char*>(rxbuffer);

    if (isdigit(message[0])) {
        String<bufferCapacity> messages[messageSpliceCount];
        String<bufferCapacity> * steeringMessage = &messages[0];
        String<bufferCapacity> * forwardMessage = &messages[1];
        String<bufferCapacity> * reverseMessage = &messages[2];

        for (uint16_t i = 0; i < messageSpliceCount && *message != '\0'; ++message) {
            if (*message == ',') messages[i++].append('\0');
            else messages[i].append(*message);
        }

        usart::print(*steeringMessage);
        usart::print(':');
        usart::print(*forwardMessage);
        usart::print(':');
        usart::print(*reverseMessage);
        usart::print('\n');
        
        int16_t steeringAngle = atoi(*steeringMessage);
        int16_t forward = atoi(*forwardMessage);
        int16_t reverse = atoi(*reverseMessage);
        
        int16_t steeringMicros = steeringClamper.mapInverselyToBounds(steeringAngle, car::servo::microsBounds);
        car::servo::setMicros(steeringMicros);
        
        int16_t reverseMicros = throttleClamper.mapInverselyToBounds(reverse, car::esc::reverseMicrosBounds);        
        if (reverseMicros != car::esc::reverseMicrosBounds.upper)
            car::esc::setMicrosReverse(reverseMicros);
        else {
            int16_t forwardMicros = throttleClamper.mapDirectlyToBounds(forward, car::esc::forwardMicrosBounds);
            car::esc::setMicrosForward(forwardMicros);
        }
    }
}
