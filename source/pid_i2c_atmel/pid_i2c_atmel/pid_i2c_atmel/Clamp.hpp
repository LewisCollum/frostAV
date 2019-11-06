#ifndef CLAMP_HPP
#define CLAMP_HPP

#include <stdint.h>

struct Bounds {
    int16_t lower;
    int16_t upper;
};

class Clamp {
    Bounds bounds;

public:
    constexpr static Clamp makeFromBounds(Bounds bounds) {
        return Clamp(bounds);
    }

    constexpr Clamp(Bounds bounds): bounds{bounds} {}

    int16_t clamp(int16_t value) {
        return (value < bounds.lower) ? bounds.lower :
            (value > bounds.upper) ? bounds.upper:
            value;
    }

    Clamp() {}
};

#endif
