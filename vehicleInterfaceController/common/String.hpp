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
    String(char* string): size{0} {
        for (; *string; ++size) 
            this->string[size] = *string++;
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
    bool operator==(const char* other) const {
        const char* stringCopy = string;
        for (const char* iter = other; *iter; ++iter) {
            if (*iter != *stringCopy++) return false;
        }
        return true;
    }
};  

#endif
