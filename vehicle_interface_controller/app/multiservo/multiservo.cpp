#include <util/delay.h>
#include "dual_servo.hpp"

int main() {
    dual_servo::start();
    
    //Arduino pin 10
    dual_servo::setMicrosB(1500);
    
    //Arduino pin 9
    dual_servo::setMicrosA(1500);

    while(1) {
        for (int i = 800; i <= 2200; i+= 20) {
            dual_servo::setMicrosA(i);
            dual_servo::setMicrosB(i);
            _delay_ms(50);
        }
    }
}
