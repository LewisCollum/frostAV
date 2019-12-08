#include <cxxtest/TestSuite.h>
#include "String.hpp"
#include <iostream>

class TestString: public CxxTest::TestSuite {
public:
    void test_volatilePointerCast() {
        volatile char message[] = "message";

        String<8> actual = const_cast<char*>(message);
        String<8> expected = "message";
        
        TS_ASSERT_SAME_DATA(actual, expected, actual.getSize());
    }

    void test_assignmentOperator() {
        String<8> actual;
        //Test for compile error
        actual = "message";
    }

    void test_copyCharPointer_sizeMatches() {
        String<8> string = "FOUR";

        int actual = string.getSize();
        int expected = 4;

        TS_ASSERT_EQUALS(actual, expected);
    }

    void test_stringComparedToCharPointer_areEqual() {
        String<8> A = "message";
        const char* B = "message";

        TS_ASSERT_EQUALS(A, B);
    }
};
