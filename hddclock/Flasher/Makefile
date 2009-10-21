DEVICE     = atmega32
CLOCK      = 16000000
OBJECTS    = src/main.o src/uart/uart.o src/uart/magicio.o

COMPILE = avr-gcc -Wall -Os -DF_CPU=$(CLOCK) -mmcu=$(DEVICE)

# symbolic targets:
all:	main.bin

upload: main.bin
	~/Development/Penguino/icyprog/icyprog --upload-flash=main.bin
	
oldupload:
	cp main.bin ~/Development/Penguino/icyprog-cs/prog.bin
	cd ~/Development/Penguino/icyprog-cs/; mono IcyProg.exe

.c.o:
	$(COMPILE) -c $< -o $@

.S.o:
	$(COMPILE) -x assembler-with-cpp -c $< -o $@

.c.s:
	$(COMPILE) -S $< -o $@

clean:
	rm -f main.bin main.elf $(OBJECTS)

main.elf: $(OBJECTS)
	$(COMPILE) -o main.elf $(OBJECTS)

main.bin: main.elf
	rm -f main.bin
	avr-objcopy -j .text -j .data -O binary main.elf main.bin

disasm:	main.elf
	avr-objdump -d main.elf
