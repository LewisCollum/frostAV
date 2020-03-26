#ifndef USART_HPP
#define USART_HPP

#include <avr/io.h>
#include <stdint.h>

namespace usart::internal {
    void setBaudRegisterWithPrescaler(uint8_t prescaler) {
        UBRR0H = prescaler >> 8;
        UBRR0L = prescaler;
    }
        
    void enableTransmitterAndReceiver() {
        UCSR0B = 1 << RXEN0 | 1 << TXEN0;
    }

    bool isTransmitBufferEmpty() {
        return UCSR0A & 1<<UDRE0;
    }

    bool isReceiveBufferEmpty() {
        return !(UCSR0A & 1<<RXC0);
    }

    void setDataBuffer(char const c) {
        UDR0 = c;
    }

    char const getDataBuffer() {
        return UDR0;
    }
}

namespace usart {
    constexpr uint32_t clockFrequency = F_CPU;
    
    void beginAtBaud(uint32_t baud) {
        uint8_t prescaler = clockFrequency/16/baud - 1;
        internal::setBaudRegisterWithPrescaler(prescaler);
        internal::enableTransmitterAndReceiver();
    }
    
    void print(char const c) {
        while (!internal::isTransmitBufferEmpty());
        internal::setDataBuffer(c);
    }
        
    void print(char const * string) {
        while (*string) print(*string++);
    }
    
    char getChar() {
        while (internal::isReceiveBufferEmpty());
        return internal::getDataBuffer();    
    }
}

#endif
