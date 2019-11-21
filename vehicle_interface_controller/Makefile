subdirs = $(shell find app -mindepth 1 -maxdepth 1 -type d)
all:
	make -C common
	for dir in $(subdirs); do make -C $$dir || exit 1; done

clean:
	make -C common $@
	for dir in $(subdirs); do make -C $$dir $@; done

test:
	make -C common $@
