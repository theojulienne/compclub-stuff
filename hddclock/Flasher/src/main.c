//
//  Foo
//
//  Created by Theo Julienne on 05.07.2009.
//  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
//

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdio.h>

#include "uart/uart.h"
#include "uart/magicio.h"


#define UART_BAUD_RATE 9600

#define BLACK 0
#define RED 1
#define GREEN 2
#define BLUE 4
#define YELLOW (RED|GREEN)
#define MAGENTA (RED|BLUE)
#define CYAN (BLUE|GREEN)
#define WHITE (RED|GREEN|BLUE)

#define DELAY 1977
//#define DELAY_FOR_60_SLITS     ((DELAY * 4) / 5)
#define DELAY_FOR_SECOND      1581
#define DELAY_FOR_60_SLITS    90000


#define SECOND_HAND_COLOUR    BLUE
#define MINUTE_HAND_COLOUR    GREEN
#define HOUR_HAND_COLOUR    RED

// interrupt: PD2 / INT0

// rev_delay?
/*
volatile uint32_t rev_delay = 0;
volatile uint16_t revCounter = 1;
*/
volatile uint8_t killMe = 0;
/*
#define COUNTER_START 0xff00
*/
/*
ISR(TIM1_OVF_vect) {
	timerOverflow++;
	TCNT1 = COUNTER_START;
	killMe = 1;
}
*/
/*
#define WINDOW_SIZE_BIT 4 // 3 bits = 8
#define WINDOW_SIZE (1<<WINDOW_SIZE_BIT)

volatile uint32_t clockAmounts[WINDOW_SIZE];
volatile uint8_t currClock = 0;

#define getTimerOverflow() (timerOverflow >> 0)

uint32_t averageClockSpeed( ) {
	int i;
	
	uint32_t sum = 0;
	
	for ( i = 0; i < WINDOW_SIZE; i++ ) {
		sum += clockAmounts[i];
	}
	
	return sum >> WINDOW_SIZE_BIT;
}
*/

volatile uint32_t countThisRevolution = 1;
volatile uint32_t lastRevolutionCounter = 1;

#define MIN_INT_COUNT 50

ISR(INT0_vect) {
	/*
	static int interruptCount = 0;
	
	if ( countThisRevolution >= MIN_INT_COUNT ) {
		interruptCount++;
		
		if ( interruptCount == 4 ) {
			lastRevolutionCounter = countThisRevolution;
			countThisRevolution = 1;

			interruptCount = 0;
		}
	}*/
	/*
	if ( countThisRevolution >= MIN_INT_COUNT ) {
		PORTA = ~PORTA;
		countThisRevolution = 0;
	}*/
	PORTA = WHITE;
	_delay_us( 1000 );
	PORTA = BLACK;
}

//TCNT1
int main(void) {
	// configure the UART (serial)
	//uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) );
	
	// enable interrupts (magic)
	sei();
	
	//rev_delay = 1;
	/*
	DDRA = 0xff;
	PORTA = 0x0;
	*/
	DDRD = 0x00;
	PORTD = (1<<PIN2);
	
	// interrupt on rising edge of INT0
	MCUCR |= (1<<ISC00) | (1<<ISC01);
	
	// enable INT0
	GICR |= ( 1 << INT0);
	
	// enable timer
	//TCCR0 = 
	//while ( 1 ) ;
	
	// enable magic stdioness
	//magicio_init( );
	
	DDRA |= WHITE;
	//DDRB |= 63;
	
	//PORTB = ~(RED | GREEN | BLUE);
	uint32_t delay = 1;
	uint32_t delayedSoFar = 0;
	int amoSecondsDone = 0;
	int color = 0;
	int i = 0;
	int colours[60] = {0};
	int amoSecondsCounted = 0;
	int amoMinutesCounted = 0;
	int placeSecondHand = 0;
	int placeMinuteHand = 0;
	int placeHourHand = 0;
	
	int tmp = 0;
	/*
	for ( i = 0; i < WINDOW_SIZE; i++ ) {
		clockAmounts[i] = 0;
	}
	*/
	for ( i = 0; i < 60; i++ ) {
		colours[i] = 0;
	}
	
	/*
	colours[placeSecondHand] = SECOND_HAND_COLOUR;
	colours[placeMinuteHand] = MINUTE_HAND_COLOUR;
	colours[placeHourHand] = HOUR_HAND_COLOUR;
	*/
	colours[placeSecondHand] = GREEN;
	
	
	PORTA = WHITE;
	
	while (!killMe) {
		//printf("hello world\r\n");
		//PORTB = ((color&7) | (color<<3));
		//PORTA = (((color&7) | (color<<3))%4);
		//color++;
		
		// outputting the colours magically
		/*i = 0;
		
		while (i < 60) {
			PORTA = colours[i];
			_delay_us ();
			i++;
		}*/
		tmp++;
		if ( tmp == 0x40 ) {
			countThisRevolution++;
			tmp = 0;
		}
		
		//uint32_t clockSpeed = lastRevCounter;//clockAmounts[currClock];//averageClockSpeed( );
		uint32_t currColour = ((uint32_t)60*(uint32_t)countThisRevolution) / (uint32_t)lastRevolutionCounter;
		//PORTA = BLACK;//colours[currColour%60];
		/// changing colours
		
		
		/*
		if ( revCounter % 10000 == 0 ) {
			colours[placeSecondHand] = 0;
			placeSecondHand++;
			if ( placeSecondHand == 60 )
				placeSecondHand = 0;
			colours[placeSecondHand] = SECOND_HAND_COLOUR;
		}
		*/
		/*
		delayedSoFar += DELAY_FOR_60_SLITS;
		if (delayedSoFar >= 1000000) {
			if (colours[placeSecondHand] == SECOND_HAND_COLOUR) {
		    	colours[placeSecondHand] = 0;
	    	}
			placeSecondHand++;
			placeSecondHand = placeSecondHand % 60;
			if (colours[placeSecondHand] == 0) {
				colours[placeSecondHand] = SECOND_HAND_COLOUR;
			}
			delayedSoFar = 0;
			amoSecondsCounted++;
			if (amoSecondsCounted == 60) {
				if (colours[placeMinuteHand] == MINUTE_HAND_COLOUR) {
			    	colours[placeMinuteHand] = 0;
		    	}
				placeMinuteHand++;
				placeMinuteHand = placeMinuteHand % 60;
				if (colours[placeMinuteHand] != HOUR_HAND_COLOUR) {
					colours[placeMinuteHand] = MINUTE_HAND_COLOUR;
				}
				amoSecondsCounted = 0;
				amoMinutesCounted++;
				if (amoMinutesCounted == 60) {
					if (colours[placeHourHand] == HOUR_HAND_COLOUR) {
				    	colours[placeHourHand] = 0;
			    	}
					placeHourHand += 5;
					placeHourHand = placeHourHand % 12;
					
					colours[placeHourHand] = HOUR_HAND_COLOUR;
					
					amoMinutesCounted = 0;
				}
			}
		}
		*/
	}
	
	PORTA = 0;
	
	return 0;
}
