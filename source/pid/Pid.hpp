#ifndef PID_HPP
#define PID_HPP

#include <stdint.h>

struct Pid {
    struct Component {
        int16_t proportional;
        int16_t integral;
        int16_t derivative;
    };

    int16_t output;

private:    
    Component gain;
    Component error;
    int16_t scale;
    
public:
    void updateError(int16_t error);
    
    static Pid makeFromGain(Component gain) {
        return Pid(gain);
    }
    
    explicit Pid(Component gain):
        output{0}, gain{gain}, error{}, scale{1} {}

    
    static Pid makeFromScaledGain(Component gain, int16_t scale) {
        return Pid(gain, scale);
    }
    
    Pid(Component gain, int16_t scale):
        output{0}, gain{gain}, error{}, scale{scale} {}
    
    Pid() {}
};

#endif
