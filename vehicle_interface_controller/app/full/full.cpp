#include <avr/io.h>
#include "String.hpp"
#include "I2C_slave.hpp"
#include "usart.hpp"
#include <stdint.h>
#include "car.hpp"
#include <stdlib.h>
#include <string.h>

constexpr int16_t bufferCapacity = 10;

void stateChange(String<bufferCapacity> state) {
    if (state == "+start")
        car::start();
    else if (state == "+stop")
        car::stop();
}

int main() {
    I2C_init(0x32);
    sei();

	while(1) {
		if (trigger == true) {
            String<bufferCapacity> message = const_cast<const char*>(rxbuffer);
            
            if (message[0] == '+') stateChange(message);
            else {
                int16_t crossTrackError = atoi(message);
                car::servo::setMicros(crossTrackError);
                car::esc::setForwardMicros(car::esc::upperBoundMicros);
            }

            trigger = false;
		}
	}
}
