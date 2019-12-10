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

    void test_mapValueToBounds_rangeTheSame() {
        Bounds<uint16_t> other = {20, 30};

        uint16_t actual = clamp.mapValueToBounds(15, other);
        uint16_t expected = 25;

        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_mapValueToBounds_rangeDifferent() {
        Bounds<uint16_t> other = {22, 28};

        uint16_t actual = clamp.mapValueToBounds(15, other);
        uint16_t expected = 25;

        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_mapValueToBounds_clampedToLowerBound() {
        Bounds<uint16_t> other = {22, 28};

        uint16_t actual = clamp.mapValueToBounds(5, other);
        uint16_t expected = 22;

        TS_ASSERT_EQUALS(actual, expected);
    }
    
    void test_mapValueToBounds_degreesToMicros() {
        Clamp<uint16_t> A = Clamp<uint16_t>::makeFromBounds({0, 180});
        Bounds<uint16_t> B = {1150, 1850};

        uint16_t actual = A.mapValueToBounds(90, B);
        uint16_t expected = 1500;

        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_mapValueToBounds_positionFromBounds() {
        Bounds<uint16_t> microsBounds = {1150, 1850};
        Bounds<uint16_t> bounds = {70, 110};
        uint16_t position = 90;
        
        Clamp<uint16_t> positionClamper = Clamp<uint16_t>::makeFromBounds(bounds);
        uint16_t actual = positionClamper.mapValueToBounds(position, microsBounds);
        uint16_t expected = 1500;
        
        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_mirrorMapValueToBounds_positionFromBoundsFlipped() {
        Bounds<int16_t> microsBounds = {1150, 1850};
        Bounds<int16_t> bounds = {70, 110};
        int16_t position = 70;
        
        Clamp<int16_t> positionClamper = Clamp<int16_t>::makeFromBounds(bounds);
        int16_t actual = positionClamper.mirrorMapValueToBounds(position, microsBounds);
        int16_t expected = 1850;
        
        TS_ASSERT_EQUALS(actual, expected);
    }    
};
