#ifndef STRING_HPP
#define STRING_HPP

#include <stdint.h>

template<int16_t capacity>
class String {
    int16_t size;
    char string[capacity];
    
public:
    void append(char c) {
        if (size < capacity) string[size++] = c;
    }
    
    String(): size{0}, string{0} {}

    void clear() {
        while (size != 0) string[--size] = 0;
    }

    operator char*() { return string; }
    operator const char*() { return string; }
};  

#endif
