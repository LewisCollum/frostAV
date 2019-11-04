#include <cxxtest/TestSuite.h>
#include "Clamp.hpp"

class TestClamp: public CxxTest::TestSuite {
    Clamp clamp;
    Bounds bounds;
    
public:
    void setUp() {
        bounds = {
            .upper = 20,
            .lower = 10
        };
        
        clamp = Clamp::makeFromBounds(bounds);
    }
    
    void test_inputAboveUpper_clampsToUpper() {
        int16_t expected = bounds.upper;
        int16_t actual = clamp.clamp(25);
        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_inputBelowLower_clampsToLower() {
        int16_t expected = bounds.lower;
        int16_t actual = clamp.clamp(5);
        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_inputBetweenBounds_noClamp() {
        int16_t expected = 15;
        int16_t actual = clamp.clamp(15);
        TS_ASSERT_EQUALS(actual, expected);
    }
};
