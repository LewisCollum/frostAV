#include "Pid.hpp"

int16_t Pid::updateError(int16_t newError) {
    error.integral += newError;
    error.derivative = newError - error.proportional;
    error.proportional = newError;
	int16_t temp = (gain.proportional*error.proportional + gain.integral*error.integral + gain.derivative*error.derivative) / scale;
    return (temp);
}
