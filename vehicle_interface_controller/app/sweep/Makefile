TARGET = sweep
.DEFAULT_GOAL = $(BUILD_DIR)/$(TARGET).hex

ROOT = ../..

include $(ROOT)/mk/toolchain.mk
include $(ROOT)/mk/default.mk

CXXFLAGS += -I$(COMMON)
OBJS += $(wildcard $(COMMON)/$(BUILD_DIR)/*.o)

include $(ROOT)/mk/rules.mk
