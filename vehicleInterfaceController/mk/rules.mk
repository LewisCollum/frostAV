$(BUILD_DIR)/%.hex: $(BUILD_DIR)/%.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

$(BUILD_DIR)/%.elf: $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: %.cpp
	mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -MMD -c $< -o $@


flash: $(BUILD_DIR)/$(TARGET).hex
	avrdude -c $(PROGRAMMER) -P $(PORT) -p $(DEVICE) -b $(FLASH_BAUD) -U flash:w:$<

test: $(TESTS)
	cxxtestgen --error-printer -o test_runner.cpp $(TESTS)
	g++ -o test_runner -I$(CXXTEST) test_runner.cpp $(TEST_SOURCES)
	./test_runner
	rm test_runner test_runner.cpp

com:
	picocom -b $(COM_BAUD) $(PORT) -p 2 --echo --omap crlf --imap crlf

clean:
	rm -rf $(BUILD_DIR)
