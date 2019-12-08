#ifndef CAR_HPP
#define CAR_HPP

#include "Clamp.hpp"
#include "dual_servo.hpp"
#include <util/delay.h>

//Arduino Uno Pins: 9 (ESC), 10 (Servo)

namespace car::servo {
    constexpr uint16_t rightBoundMicros = 1150;
    constexpr uint16_t leftBoundMicros = 1850;
    constexpr uint16_t centerMicros = 1500;
    constexpr Bounds<uint16_t> microsBounds = {
        .lower = rightBoundMicros,
        .upper = leftBoundMicros};

    uint16_t currentMicros;     
    
    namespace {
        Clamp clamper = Clamp<uint16_t>::makeFromBounds(microsBounds);
    }
    
    void setMicros(uint16_t micros) {
        dual_servo::setMicrosB(currentMicros = clamper.clamp(micros));
    }

    void center() {
        dual_servo::setMicrosB(currentMicros = centerMicros);
    }

    void increment(int16_t increment) {
        setMicros(currentMicros += increment);
    }

    bool isAtLeftBound() { return currentMicros == microsBounds.upper; }
    bool isAtRightBound() { return currentMicros == microsBounds.lower; }
    bool isCentered() { return currentMicros == centerMicros; }
}

namespace car::esc {
    constexpr uint16_t upperBoundMicros = 1600;
    constexpr uint16_t lowerBoundMicros = 1420;
    constexpr uint16_t centerMicros = 1500;
    constexpr Bounds<uint16_t> forwardMicrosBounds = {
        .lower = centerMicros,
        .upper = upperBoundMicros};
    constexpr Bounds<uint16_t> reverseMicrosBounds = {
        .lower = lowerBoundMicros,
        .upper = centerMicros};

    uint16_t currentMicros; 
    
    namespace {
        Clamp forwardClamper = Clamp<uint16_t>::makeFromBounds(forwardMicrosBounds);
        Clamp reverseClamper = Clamp<uint16_t>::makeFromBounds(reverseMicrosBounds);

        void setMicrosToArm() {
            dual_servo::setMicrosA(currentMicros = centerMicros);
        }
    }
    
    void setMicrosForward(uint16_t micros) {
        dual_servo::setMicrosA(currentMicros = forwardClamper.clamp(micros));
    }
    
    void setMicrosReverse(uint16_t micros) {
        dual_servo::setMicrosA(currentMicros = reverseClamper.clamp(micros));
    }

    void arm() {
        setMicrosToArm();
        _delay_ms(1500);
    }

    void brake() {
        dual_servo::setMicrosA(currentMicros = lowerBoundMicros);
        _delay_ms(1000);
        dual_servo::setMicrosA(currentMicros = centerMicros);
    }

    void increment(int16_t increment) {
        currentMicros += increment;
        setMicrosForward(currentMicros);
    }

    bool isAtUpperBound() { return currentMicros == forwardMicrosBounds.upper; }
    bool isAtLowerBound() { return currentMicros == reverseMicrosBounds.lower; }
    bool isCentered() { return currentMicros == centerMicros; }
}

namespace car {
    void start() {
        dual_servo::start();
        car::servo::center();
        car::esc::arm();
    }

    void stop() {
        car::servo::center();
        car::esc::brake();
    }
}

#endif
