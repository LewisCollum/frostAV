#include <avr/io.h>
#include <util/delay.h>

constexpr uint8_t prescaler = 8;
constexpr uint32_t clockFrequency = F_CPU;
constexpr uint8_t pwmFrequency = 50;

static constexpr uint32_t microsToCycles(uint16_t micros) {
    constexpr uint32_t unitConversion = 1E6;
    return (clockFrequency/unitConversion/prescaler) * micros;
}

static constexpr uint32_t hertzToCycles(uint16_t hertz) {
    return clockFrequency/prescaler/hertz;
}

int main() {
	DDRB |= 1 << PINB1; //Set pin 9 on arduino to output

	TCCR1A |=
        1 << WGM11 | //PWM Mode 14 (1/3)
        1 << COM1A0 | //Inverting Mode (1/2)
        1 << COM1A1; //Inverting Mode (2/2)
    
	TCCR1B |=
        1 << WGM12 | //PWM Mode 14 (2/3)
        1 << WGM13 | //PWM Mode 14 (3/3)
        1 << CS11; //Prescaler: 8

	ICR1 = hertzToCycles(pwmFrequency)-1;

	while(1) {
		OCR1A = ICR1 - microsToCycles(2000);
		_delay_ms(1000);
		OCR1A = ICR1 - microsToCycles(1000);
		_delay_ms(1000);
	}

	return 0;
}
