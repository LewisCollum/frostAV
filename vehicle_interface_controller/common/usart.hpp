#ifndef USART_HPP
#define USART_HPP

#include <avr/io.h>
#include <stdint.h>

namespace usart {
    constexpr uint32_t clockFrequency = F_CPU;

    void beginAtBaud(uint32_t baud) {
        uint8_t ubrr = clockFrequency/16/baud - 1;
        UBRR0H = ubrr >> 8;
        UBRR0L = ubrr;

        //Enable Transmitter & Receiver
        UCSR0B = 1 << RXEN0 | 1 << TXEN0;
        //Frame Format: 8 data, 2 stop
        UCSR0C = 3 << UCSZ00;	//1 << USBS0 | 3 << UCSZ00;

    }

    void print(char const c) {
        while (!(UCSR0A & 1<<UDRE0));
        UDR0 = c;    
    }
        
    void print(char const * string) {
        while (*string) print(*string++);
    }
    
    char getChar() {
        while (!(UCSR0A & 1<<RXC0));
        return UDR0;    
    }
}

#endif
