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

    T clamp(T value) {
        return (value < bounds.lower) ? bounds.lower :
            (value > bounds.upper) ? bounds.upper:
            value;
    }
    
    T mapDirectlyToBounds(T value, Bounds<T> other) {
        T otherRange = other.upper - other.lower;
        T thisRange = bounds.upper - bounds.lower;
        
        return other.lower + otherRange*(clamp(value) - bounds.lower)/thisRange;
    }

    T mapInverselyToBounds(T value, Bounds<T> other) {
        T inverse = bounds.upper-value + bounds.lower;
        return mapDirectlyToBounds(inverse, other);
    }
    
    Clamp() {}
};

#endif
