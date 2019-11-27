#ifndef CAR_HPP
#define CAR_HPP

#include "Clamp.hpp"
#include "dual_servo.hpp"

namespace car {
    void start() {
        dual_servo::start();
    }
}

namespace car::servo {
    namespace {
        Clamp clamper = Clamp::makeFromBounds({
                .lower = 1100,
                .upper = 1900});
    }
    
    void setMicros(uint16_t micros) {
        dual_servo::setMicrosB(clamper.clamp(micros));
    }
}

namespace car::esc {
    namespace {
        Clamp forwardClamper = Clamp::makeFromBounds({
                .lower = 1500,
                .upper = 1580});

        Clamp reverseClamper = Clamp::makeFromBounds({
                .lower = 1420,
                .upper = 1500});
    }

    void setMicrosForward(uint16_t micros) {
        dual_servo::setMicrosA(forwardClamper.clamp(micros));
    }
    
    void setMicrosReverse(uint16_t micros) {
        dual_servo::setMicrosA(reverseClamper.clamp(micros));
    }

    void setMicrosToArm() {
        dual_servo::setMicrosA(1500);
    }
}

#endif
