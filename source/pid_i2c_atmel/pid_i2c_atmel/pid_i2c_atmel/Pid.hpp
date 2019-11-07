#ifndef PID_HPP
#define PID_HPP

#include <stdint.h>

struct Pid {
    struct Component {
        int16_t proportional;
        int16_t integral;
        int16_t derivative;
    };

private:    
    Component gain;
    Component error;
    int16_t scale;
    
public:
    int16_t updateError(int16_t error);
    
    constexpr static Pid makeFromGain(Component gain) {
        return Pid(gain);
    }
    
    constexpr explicit Pid(Component gain):
        gain{gain}, error{}, scale{1} {}

    
    constexpr static Pid makeFromScaledGain(int16_t scale, Component gain) {
        return Pid(scale, gain);
    }
    
    constexpr Pid(int16_t scale, Component gain):
        gain{gain}, error{}, scale{scale} {}

    Pid() {}
};

#endif