#include <cxxtest/TestSuite.h>
#include "Pid.hpp"

class TestPid: public CxxTest::TestSuite {
public:
    void test_errorInput_returnsCorrectedOutput() {
        Pid pid = Pid::makeFromGain({
                .proportional = 1,
                .integral = 2,
                .derivative = 3 });
        
        int16_t actual = pid.updateError(2);
        int16_t expected = 12;

        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_scaledGain() {
        int16_t scale = 100;
        
        Pid pid = Pid::makeFromScaledGain(scale, {
                .proportional = 100,
                .integral = 200,
                .derivative = 300 });
        
        int16_t actual = pid.updateError(2);
        int16_t expected = 12;

        TS_ASSERT_EQUALS(actual, expected);
    }
};
