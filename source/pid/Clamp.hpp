#ifndef CLAMP_HPP
#define CLAMP_HPP

#include <stdint.h>

struct Bounds {
    int16_t upper;
    int16_t lower;
};

class Clamp {
    Bounds bounds;

public:
    static Clamp makeFromBounds(Bounds bounds) {
        return Clamp(bounds);
    }

    Clamp(Bounds bounds): bounds{bounds} {}
    Clamp() {}
    int16_t clamp(int16_t value) {
        if (value >= bounds.upper) return bounds.upper;
        else if (value <= bounds.lower) return bounds.lower;
        else return value;
    }
};

#endif
