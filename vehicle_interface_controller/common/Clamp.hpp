#ifndef CLAMP_HPP
#define CLAMP_HPP

#include <stdint.h>

template<typename T>
struct Bounds {
    T lower;
    T upper;
};

template<typename T>
class Clamp {
    Bounds<T> bounds;

public:
    constexpr static Clamp<T> makeFromBounds(Bounds<T> bounds) {
        return Clamp(bounds);
    }

    constexpr explicit Clamp(Bounds<T> bounds): bounds{bounds} {}

    int16_t clamp(T value) {
        return (value < bounds.lower) ? bounds.lower :
            (value > bounds.upper) ? bounds.upper:
            value;
    }

    Clamp() {}
};

#endif
