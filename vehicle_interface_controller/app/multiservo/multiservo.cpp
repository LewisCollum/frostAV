#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "Pid.hpp"
#include "Clamp.hpp"
#include "String.hpp"
#include "usart.hpp"

constexpr uint8_t prescaler = 8;
constexpr uint32_t clockFrequency = F_CPU;
constexpr uint8_t pwmFrequency = 50;
constexpr uint32_t baud = 9600;

static constexpr uint32_t microsToCycles(uint16_t micros) {
    constexpr uint32_t unitConversion = 1E6;
    return (clockFrequency/unitConversion/prescaler) * micros;
}

static constexpr uint32_t hertzToCycles(uint16_t hertz) {
    return clockFrequency/prescaler/hertz;
}

static void setupServoPwm() {
	DDRB |= 1 << PINB1; //Output pin 9 (Arduino)
    DDRB |= 1 << PINB2; //Output pin 10 (Arduino)

	TCCR1A |=
        1 << WGM11 | //PWM Mode 14 (1/3)
        1 << COM1A1 | //Non-Inverting Mode
        1 << COM1B1; //Non-Inverting Mode
    
	TCCR1B |=
        1 << WGM12 | //PWM Mode 14 (2/3)
        1 << WGM13 | //PWM Mode 14 (3/3)
        1 << CS11; //Prescaler: 8

	ICR1 = hertzToCycles(pwmFrequency)-1;
}


int main() {
    setupServoPwm();

    //OCR1B corresponds to PINB2 (Arduino pin 10). Hooked up to steering servo.
    OCR1B = microsToCycles(2000);
    
    //OCR1A corresponds to PINB1 (Arduino pin 9). Hooked up to ESC for motor.
    OCR1A = microsToCycles(1500);
    _delay_ms(1000); //Wait for arming sequence

    while(1) {
        for (int i = 800; i <= 2200; ++i) {
            OCR1A = microsToCycles(i);
            OCR1B = microsToCycles(i);
            _delay_ms(1);
        }
    }
}
