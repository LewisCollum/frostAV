#include <avr/io.h>
#include <stdint.h>
#include <stdlib.h>

#include "car.hpp"

int main() {
    car::start();
	while(1) {
        for (uint16_t i = car::servo::microsBounds.lower; i <= car::servo::microsBounds.upper; i += 10) {
            car::servo::setMicros(i);
            _delay_ms(20);
        }
        for (uint16_t i = car::servo::microsBounds.upper; i >= car::servo::microsBounds.lower; i -= 10) {
            car::servo::setMicros(i);
            _delay_ms(20);
        }        

    }
}
