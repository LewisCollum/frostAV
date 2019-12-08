#include <cxxtest/TestSuite.h>
#include "Clamp.hpp"

class TestClamp: public CxxTest::TestSuite {
    Clamp<uint16_t> clamp;
    Bounds<uint16_t> bounds;
    
public:
    void setUp() {
        bounds = {
            .lower = 10,
            .upper = 20
        };
        
        clamp = Clamp<uint16_t>::makeFromBounds(bounds);
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
