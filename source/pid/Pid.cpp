#include "Pid.hpp"

void Pid::updateError(int16_t newError) {
    error.integral += newError;
    error.derivative = newError - error.proportional;
    error.proportional = newError;

    output = -(gain.proportional*error.proportional +
               gain.integral*error.integral +
               gain.derivative*error.derivative) / scale ;
}
