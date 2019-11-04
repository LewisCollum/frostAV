#include <cxxtest/TestSuite.h>
#include "Pid.hpp"

class TestPid: public CxxTest::TestSuite {
    Pid pid;
    
public:
    void test_errorInput_returnsCorrectedOutput() {
        pid = Pid::makeFromGain({1, 2, 3});
        pid.updateError(2);
        TS_ASSERT_EQUALS(pid.output, -12);
    }

    void test_scaledGain() {
        pid = Pid::makeFromScaledGain({100, 200, 300}, 100);
        pid.updateError(2);
        TS_ASSERT_EQUALS(pid.output, -12);
    }
};
