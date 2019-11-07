BIN=sweep

CPP = $(BIN).cpp $(wildcard *.cpp)
OBJ = $(CPP:%.cpp=%.o)
DEP = $(OBJ:%.o=%.d)

CROSS_COMPILE=avr-
CXX=$(CROSS_COMPILE)g++
OBJCOPY=$(CROSS_COMPILE)objcopy
CXXFLAGS=-Os -Wall -DF_CPU=$(F_CPU) -mmcu=atmega328p -std=gnu++17

F_CPU=16000000UL
PORT=/dev/ttyACM0
DEVICE=ATMEGA328P
PROGRAMMER=arduino
FLASH_BAUD=115200
COM_BAUD=9600

TESTS = TestPid.hpp TestClamp.hpp
TEST_SOURCES= Pid.cpp
TEST_RUNNER = runner



$(BIN).hex: $(BIN).elf
	${OBJCOPY} -O ihex -R .eeprom $< $@

$(BIN).elf: $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

-include $(DEP)

%.o: %.cpp
	 $(CXX) $(CXXFLAGS) -MMD -c $< -o $@ 

flash: $(BIN).hex
	avrdude -c $(PROGRAMMER) -P $(PORT) -p $(DEVICE) -b $(FLASH_BAUD) -U flash:w:$<

test: $(TESTS)
	cxxtestgen --error-printer -o $(TEST_RUNNER).cpp $(TESTS)
	g++ -o $(TEST_RUNNER) -I$CXXTEST $(TEST_RUNNER).cpp $(TEST_SOURCES)
	./$(TEST_RUNNER)

com:
	picocom -b $(COM_BAUD) $(PORT) -p 2 --echo --omap crlf --imap crlf

clean:
	rm -f ${BIN}.elf ${BIN}.hex $(OBJ) $(TEST_RUNNER)* $(DEP)

.PHONY: clean
