F_CPU=16000000UL
BIN=sweep
OBJS=sweep.o Pid.o
TESTS = TestPid.hpp TestClamp.hpp
TEST_SOURCES= Pid.cpp
TEST_RUNNER = runner

CXX=avr-g++
OBJCOPY=avr-objcopy
CXXFLAGS=-Os -Wall -DF_CPU=$(F_CPU) -mmcu=atmega328p -std=gnu++17
port=/dev/ttyACM0

avrDevice=ATMEGA328P
programmer=arduino
baud=115200


${BIN}.hex: ${BIN}.elf
	${OBJCOPY} -O ihex -R .eeprom $< $@

${BIN}.elf: ${OBJS}
	${CXX} -o $@ $^

install: ${BIN}.hex
	avrdude -c ${programmer} -P ${port} -p ${avrDevice} -b ${baud} -U flash:w:$<

test: $(TESTS)
	cxxtestgen --error-printer -o $(TEST_RUNNER).cpp $(TESTS)
	g++ -o $(TEST_RUNNER) -I$CXXTEST $(TEST_RUNNER).cpp $(TEST_SOURCES)
	./$(TEST_RUNNER)

clean:
	rm -f ${BIN}.elf ${BIN}.hex ${OBJS} $(TEST_RUNNER)*
