#ifndef CYCLES_HPP
#define CYCLES_HPP

namespace Cycles {
    constexpr uint32_t clockFrequency = F_CPU;
    static uint8_t prescaler;

    uint32_t fromMicros(uint16_t micros) {
        constexpr uint32_t unitConversion = 1E6;
        return (clockFrequency/unitConversion/prescaler) * micros;
    }

    uint32_t fromHertz(uint16_t hertz) {
        return clockFrequency/prescaler/hertz;
    }    
}

#endif
