# Makefile for NMP Memory Benchmarks

# Compiler settings
CC = gcc
CFLAGS = -O2 -static -Wall
M5_PATH = ../util/m5
GEM5_INCLUDE = ../include

# gem5 m5ops library and header paths
M5_INCLUDE = -I$(GEM5_INCLUDE)
M5_LIB = $(M5_PATH)/build/x86/out/libm5.a

# Targets
TARGETS = memory_stride_access nmp_device_test nmp_ptr_chase_test device_cxl_test \
          host_offload device_offload cache_probe graph_walk_host

all: $(TARGETS)

# Build with m5ops (always linked with libm5.a)
memory_stride_access: memory_stride_access.c
	@if [ ! -f "$(M5_LIB)" ]; then \
		echo "Building m5ops library..."; \
		cd $(M5_PATH) && scons build/x86/out/libm5.a; \
	fi
	$(CC) $(CFLAGS) $(M5_INCLUDE) -o $@ $< $(M5_LIB)
	@echo "Built: $@ (with m5ops linked)"

nmp_device_test: nmp_device_test.c
	@if [ ! -f "$(M5_LIB)" ]; then \
		echo "Building m5ops library..."; \
		cd $(M5_PATH) && scons build/x86/out/libm5.a; \
	fi
	$(CC) $(CFLAGS) $(M5_INCLUDE) -o $@ $< $(M5_LIB)
	@echo "Built: $@ (with m5ops linked)"

nmp_ptr_chase_test: nmp_ptr_chase_test.c
	@if [ ! -f "$(M5_LIB)" ]; then \
		echo "Building m5ops library..."; \
		cd $(M5_PATH) && scons build/x86/out/libm5.a; \
	fi
	$(CC) $(CFLAGS) $(M5_INCLUDE) -o $@ $< $(M5_LIB)
	@echo "Built: $@ (with m5ops linked)"

# Device-side userspace test: mmap /dev/mem over the CXL range
# and round-trip a 64-bit pattern to validate cxl_mem_bus access.
device_cxl_test: device_cxl_test.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "Built: $@"

# --- OP_EXEC_BLOB code blob -------------------------------------------------
# Freestanding, position-independent raw .text shipped through the mailbox and
# executed on the device (see blob_fnv.c for the discipline). Flags keep the
# emitted code relocation-free: no stack-protector ref, no CET endbr, no
# unwind tables, no PIC/GOT.
BLOB_CFLAGS = -ffreestanding -fno-pic -fno-stack-protector \
              -fcf-protection=none -fno-asynchronous-unwind-tables \
              -fno-unwind-tables -Os

blob_fnv.o: blob_fnv.c blob_abi.h
	$(CC) $(BLOB_CFLAGS) -c -o $@ $<

# Verify gate, THEN extract raw .text. Fails the build if the blob would not
# be position-independent (any .text relocation) or if entry isn't at offset 0.
blob.bin: blob_fnv.o
	@if objdump -r $< | grep -q 'RELOCATION RECORDS FOR \[.text\]'; then \
		echo "ERROR: blob .text has relocations — not position-independent:"; \
		objdump -r $<; exit 1; \
	fi
	@objdump -d $< | grep -qE '^0+ <entry>:' || { \
		echo "ERROR: 'entry' is not at .text offset 0:"; objdump -d $<; exit 1; }
	objcopy -O binary -j .text $< $@
	@echo "Built: $@ ($$(wc -c < $@) bytes), entry@0, no .text relocs"

# Bake the blob bytes into a C header (cxl_blob[] / cxl_blob_len) for the host.
# xxd names the array after the file ("blob_bin"); rename to cxl_blob.
blob_bytes.h: blob.bin
	xxd -i $< > $@
	sed -i 's/blob_bin/cxl_blob/g' $@
	@echo "Generated: $@"

# XTEA cipher blob — same freestanding flags + verify gate as the FNV blob.
blob_xtea.o: blob_xtea.c blob_abi.h
	$(CC) $(BLOB_CFLAGS) -c -o $@ $<

blob_xtea.bin: blob_xtea.o
	@if objdump -r $< | grep -q 'RELOCATION RECORDS FOR \[.text\]'; then \
		echo "ERROR: blob .text has relocations — not position-independent:"; \
		objdump -r $<; exit 1; \
	fi
	@objdump -d $< | grep -qE '^0+ <entry>:' || { \
		echo "ERROR: 'entry' is not at .text offset 0:"; objdump -d $<; exit 1; }
	objcopy -O binary -j .text $< $@
	@echo "Built: $@ ($$(wc -c < $@) bytes), entry@0, no .text relocs"

blob_xtea_bytes.h: blob_xtea.bin
	xxd -i $< > $@
	sed -i 's/blob_xtea_bin/cxl_blob_xtea/g' $@
	@echo "Generated: $@"

# Graph random-walk blob (config 2 of the CXL graph-walk comparison) —
# same freestanding flags + verify gate as the FNV/XTEA blobs. The
# kernel is gw_walk() from graph_walk.h, the SAME inline function the
# host executor compiles.
blob_walk.o: blob_walk.c blob_abi.h graph_walk.h
	$(CC) $(BLOB_CFLAGS) -c -o $@ $<

blob_walk.bin: blob_walk.o
	@if objdump -r $< | grep -q 'RELOCATION RECORDS FOR \[.text\]'; then \
		echo "ERROR: blob .text has relocations — not position-independent:"; \
		objdump -r $<; exit 1; \
	fi
	@objdump -d $< | grep -qE '^0+ <entry>:' || { \
		echo "ERROR: 'entry' is not at .text offset 0:"; objdump -d $<; exit 1; }
	objcopy -O binary -j .text $< $@
	@echo "Built: $@ ($$(wc -c < $@) bytes), entry@0, no .text relocs"

blob_walk_bytes.h: blob_walk.bin
	xxd -i $< > $@
	sed -i 's/blob_walk_bin/cxl_blob_walk/g' $@
	@echo "Generated: $@"

# Host->device CXL offload: shared-memory mailbox + doorbell.
# Both link no m5ops; both depend on the shared mailbox contract header.
# host_offload bakes in the blob (blob_bytes.h); device_offload needs the
# blob entry ABI (blob_abi.h).
host_offload: host_offload.c cxl_mailbox.h blob_bytes.h blob_xtea_bytes.h
	$(CC) $(CFLAGS) -o $@ $<
	@echo "Built: $@"

device_offload: device_offload.c cxl_mailbox.h blob_abi.h graph_walk.h
	$(CC) $(CFLAGS) -o $@ $<
	@echo "Built: $@"

# CXL graph-walk comparison, host side (both configs). Links libm5 for
# the m5_reset_stats/m5_dump_stats brackets (memory_stride_access
# precedent).
graph_walk_host: graph_walk_host.c cxl_mailbox.h graph_walk.h blob_walk_bytes.h
	@if [ ! -f "$(M5_LIB)" ]; then \
		echo "Building m5ops library..."; \
		cd $(M5_PATH) && scons build/x86/out/libm5.a; \
	fi
	$(CC) $(CFLAGS) $(M5_INCLUDE) -o $@ $< $(M5_LIB)
	@echo "Built: $@ (with m5ops linked)"

# Host-side cacheability probe for /dev/mem mappings of a Reserved
# CXL carve (O_SYNC vs no-O_SYNC). Standalone, no m5ops.
cache_probe: cache_probe.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "Built: $@"

# Clean
clean:
	rm -f $(TARGETS) *.o blob.bin blob_bytes.h blob_xtea.bin blob_xtea_bytes.h \
	      blob_walk.bin blob_walk_bytes.h

# Install to disk image (requires mount)
install: $(TARGETS)
	@if [ -d "/tmp/parsec_mount/home/cxl_benchmark" ]; then \
		echo "Installing to disk image..."; \
		sudo cp memory_stride_access /tmp/parsec_mount/home/cxl_benchmark/memory_stride_access; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/memory_stride_access; \
		echo "Installed: /home/cxl_benchmark/memory_stride_access"; \
		sudo cp nmp_device_test /tmp/parsec_mount/home/cxl_benchmark/nmp_device_test; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/nmp_device_test; \
		echo "Installed: /home/cxl_benchmark/nmp_device_test"; \
		sudo cp nmp_ptr_chase_test /tmp/parsec_mount/home/cxl_benchmark/nmp_ptr_chase_test; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/nmp_ptr_chase_test; \
		echo "Installed: /home/cxl_benchmark/nmp_ptr_chase_test"; \
		sudo cp host_offload /tmp/parsec_mount/home/cxl_benchmark/host_offload; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/host_offload; \
		echo "Installed: /home/cxl_benchmark/host_offload"; \
		sudo cp device_offload /tmp/parsec_mount/home/cxl_benchmark/device_offload; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/device_offload; \
		echo "Installed: /home/cxl_benchmark/device_offload"; \
		sudo cp cache_probe /tmp/parsec_mount/home/cxl_benchmark/cache_probe; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/cache_probe; \
		echo "Installed: /home/cxl_benchmark/cache_probe"; \
		sudo cp graph_walk_host /tmp/parsec_mount/home/cxl_benchmark/graph_walk_host; \
		sudo chmod +x /tmp/parsec_mount/home/cxl_benchmark/graph_walk_host; \
		echo "Installed: /home/cxl_benchmark/graph_walk_host"; \
	else \
		echo "ERROR: Disk image not mounted at /tmp/parsec_mount"; \
		echo "Run: sudo mount -o loop,offset=\$$((2048*512)) fs_files/parsec.img /tmp/parsec_mount"; \
	fi

.PHONY: all clean install
