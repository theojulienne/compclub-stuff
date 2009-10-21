#include <avr/io.h>
#include <stdio.h>
#include "uart.h"

static int my_stdio_putchar( char c, FILE *stream ) {
	uart_putc( c );
	
	return 0;
}

FILE uart_out = FDEV_SETUP_STREAM( my_stdio_putchar, NULL, _FDEV_SETUP_WRITE );

void magicio_init( ) {
	stdout = &uart_out;
}
