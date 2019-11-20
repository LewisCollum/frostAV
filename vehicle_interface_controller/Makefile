BUILD_DIR = ./build
LOCAL_LIB = ./lib

SRCS := $(wildcard $(LOCAL_LIB)/*.cpp)
OBJS := $(SRCS:%.cpp=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

CROSS_COMPILE = avr-
CXX = $(CROSS_COMPILE)g++
OBJCOPY = $(CROSS_COMPILE)objcopy
CXXFLAGS = -Os -Wall -DF_CPU=$(F_CPU) -mmcu=atmega328p -std=gnu++17 -I,$(LOCAL_LIB)

#Device
F_CPU = 16000000UL
PORT = /dev/ttyACM0
DEVICE = ATMEGA328P
PROGRAMMER = arduino
FLASH_BAUD = 115200
COM_BAUD = 9600

#Unit Testing
TESTS = TestPid.hpp TestClamp.hpp
TEST_SOURCES = Pid.cpp
TEST_RUNNER = runner

$(BUILD_DIR)/$(TARGET).hex: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

-include $(DEPS)

$(BUILD_DIR)/%.o: %.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -MMD -c $< -o $@ 

flash: $(TARGET).hex
	avrdude -c $(PROGRAMMER) -P $(PORT) -p $(DEVICE) -b $(FLASH_BAUD) -U flash:w:$<

test: $(TESTS)
	cxxtestgen --error-printer -o $(TEST_RUNNER).cpp $(TESTS)
	g++ -o $(TEST_RUNNER) -I$CXXTEST $(TEST_RUNNER).cpp $(TEST_SOURCES)
	./$(TEST_RUNNER)

com:
	picocom -b $(COM_BAUD) $(PORT) -p 2 --echo --omap crlf --imap crlf

clean:
	rm -rf $(BUILD_DIR)

.PHONY: clean
