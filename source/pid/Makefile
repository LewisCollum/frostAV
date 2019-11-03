F_CPU=16000000UL
BIN=sweep
OBJS=sweep.o

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

clean:
	rm -f ${BIN}.elf ${BIN}.hex ${OBJS}
