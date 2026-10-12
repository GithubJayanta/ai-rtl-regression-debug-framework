SIM ?= verilator
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../rtl/fifo.v
TOPLEVEL = fifo
MODULE = test_fifo
EXTRA_ARGS += -Wno-fatal
VERILATOR_TRACE = 1
ifeq ($(BUG),1)
COMPILE_ARGS += -DBUG
endif
include $(shell cocotb-config --makefiles)/Makefile.sim
