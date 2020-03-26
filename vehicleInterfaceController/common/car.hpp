#ifndef CAR_HPP
#define CAR_HPP

#include "Clamp.hpp"
#include "dual_servo.hpp"
#include <util/delay.h>

//Arduino Uno Pins: 9 (ESC, MicrosA), 10 (Servo, MicrosB)

namespace car {
    using MicrosType = int16_t;
}

namespace car::servo {
    //Calibration Parameters
    constexpr MicrosType rightBoundMicros = 1300;
    constexpr MicrosType leftBoundMicros = 2000;
    constexpr MicrosType centerMicros = 1650;
    
    constexpr Bounds<MicrosType> microsBounds = {
        .lower = rightBoundMicros,
        .upper = leftBoundMicros};

    MicrosType currentMicros;     
    
    namespace internal {
        Clamp clamper = Clamp<MicrosType>::makeFromBounds(microsBounds);
    }
    
    void setMicros(MicrosType micros) {
        dual_servo::setMicrosB(currentMicros = internal::clamper.clamp(micros));
    }
        
    void center() {
        dual_servo::setMicrosB(currentMicros = centerMicros);
    }

    void increment(MicrosType increment) {
        setMicros(currentMicros += increment);
    }

    bool isAtLeftBound() { return currentMicros == microsBounds.upper; }
    bool isAtRightBound() { return currentMicros == microsBounds.lower; }
    bool isCentered() { return currentMicros == centerMicros; }
}

namespace car::esc {
    constexpr MicrosType upperBoundMicros = 1650;
    constexpr MicrosType lowerBoundMicros = 1250;
    constexpr MicrosType centerMicros = 1500;
    constexpr Bounds<MicrosType> forwardMicrosBounds = {
        .lower = centerMicros,
        .upper = upperBoundMicros};
    constexpr Bounds<MicrosType> reverseMicrosBounds = {
        .lower = lowerBoundMicros,
        .upper = centerMicros};

    MicrosType currentMicros; 
    
    namespace internal {
        Clamp forwardClamper = Clamp<MicrosType>::makeFromBounds(forwardMicrosBounds);
        Clamp reverseClamper = Clamp<MicrosType>::makeFromBounds(reverseMicrosBounds);

        void setMicrosToArm() {
            dual_servo::setMicrosA(currentMicros = centerMicros);
        }
    }
    
    void setMicrosForward(MicrosType micros) {
        dual_servo::setMicrosA(currentMicros = internal::forwardClamper.clamp(micros));
    }
    
    void setMicrosReverse(MicrosType micros) {
        dual_servo::setMicrosA(currentMicros = internal::reverseClamper.clamp(micros));
    }

    void arm() {
        internal::setMicrosToArm();
        _delay_ms(2000);
    }

    void brake() {
        dual_servo::setMicrosA(currentMicros = lowerBoundMicros);
        _delay_ms(1000);
        dual_servo::setMicrosA(currentMicros = centerMicros);
    }

    void increment(MicrosType increment) {
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
