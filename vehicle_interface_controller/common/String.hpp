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
    String(const char* string): size{0} {
        char* copy = const_cast<char*>(string);
        for (; *copy; ++size)
            this->string[size] = *copy++;
    }
    
    void clear() {
        while (size != 0) string[--size] = 0;
    }

    const char& operator[](int i) {
        return string[i];
    }
    
    int16_t getSize() const { return size; }
    operator char*() { return string; }
    operator const char*() { return string; }
    operator const void*() { return string; }    
};  

#endif
