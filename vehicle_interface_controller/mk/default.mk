SRCS += $(wildcard *.cpp)
OBJS += $(SRCS:%.cpp=$(BUILD_DIR)/%.o)
DEPS += $(OBJS:.o=.d)
-include $(DEPS)
