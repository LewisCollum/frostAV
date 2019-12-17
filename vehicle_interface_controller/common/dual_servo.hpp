#ifndef DUALSERVO_HPP
#define DUALSERVO_HPP

#include <avr/io.h>
#include "cycles.hpp"

namespace dual_servo {
    void start() {
        DDRB |= 1 << PINB1; //Output from OCR1A (pin 9 Arduino Uno)
        DDRB |= 1 << PINB2; //Output from OCR1B (pin 10 Arduino Uno) 

        TCCR1A |=
            1 << WGM11 | //PWM Mode 14 (1/3)
            1 << COM1A1 | //Non-Inverting Mode
            1 << COM1B1; //Non-Inverting Mode
    
        TCCR1B |=
            1 << WGM12 | //PWM Mode 14 (2/3)
            1 << WGM13 | //PWM Mode 14 (3/3)
            1 << CS11; //Prescaler: 8

        cycles::prescaler = 8;
        ICR1 = cycles::fromHertz(50)-1;
    }

    void setMicrosA(uint16_t micros) {    
        OCR1A = cycles::fromMicros(micros);
    }

    void setMicrosB(uint16_t micros) {
        OCR1B = cycles::fromMicros(micros);
    }
}

#endif
