#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include <string.h>
//#include "Pid.hpp"
#include "Clamp.hpp"

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
	DDRB |= 1 << PINB1; //Set pin 9 on arduino to output

	TCCR1A |=
        1 << WGM11 | //PWM Mode 14 (1/3)
        1 << COM1A0 | //Inverting Mode (1/2)
        1 << COM1A1; //Inverting Mode (2/2)
    
	TCCR1B |=
        1 << WGM12 | //PWM Mode 14 (2/3)
        1 << WGM13 | //PWM Mode 14 (3/3)
        1 << CS11; //Prescaler: 8

    //50Hz PWM to cycles for servo
	ICR1 = hertzToCycles(pwmFrequency)-1;
}

static void putChar(char c) {
    while (!(UCSR0A & 1<<UDRE0));
    UDR0 = c;    
}

static void putString(char* string) {
    while (*string) putChar(*string++);
}

static void print(char* string) {
    putString(string);
    putChar('\n');
}

static char getChar() {
    while (!(UCSR0A & 1<<RXC0));
    return UDR0;    
}

template<int16_t capacity>
class String {
    int16_t size;
    char string[capacity];
    
public:
    void append(char c) {
        if (size < capacity) string[size++] = c;
    }
    
    String(): size{0}, string{0} {}

    void clear() {
        memset(string, 0, size);
        size = 0;
    }

    operator char*() { return string; }
    operator const char*() { return string; }
};


int main() {
    
    Clamp steeringClamp = Clamp(Bounds{
            .lower = 750,
            .upper = 2200
        });


    setupServoPwm();

    uint8_t ubrr = clockFrequency/16/baud - 1;
    UBRR0H = ubrr >> 8;
    UBRR0L = ubrr;

    //Enable Transmitter & Receiver
    UCSR0B = 1 << RXEN0 | 1 << TXEN0;
    //Frame Format: 8 data, 2 stop
    UCSR0C = 1 << USBS0 | 3 << UCSZ00;

    String<10> message;
    char currentChar;
	while(1) {
        currentChar = getChar();
        if (currentChar != '\n') {
            message.append(currentChar);
        }
        else {
            print(message);
            int16_t packet = atoi(message);
            int16_t servoMicros = steeringClamp.clamp(packet);

            OCR1A = ICR1 - microsToCycles(servoMicros);
            _delay_ms(1000);
            message.clear();
        } 
	}
}
