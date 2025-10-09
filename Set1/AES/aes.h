#ifndef AES_H
#define AES_H


#include <stdio.h>
#include <stdint.h>

void sub_bytes(uint8_t state [4][4]);
void mix_columns(uint8_t state[4][4]);
static uint8_t gf_mult(uint8_t a, uint8_t b) ;
void ruota_Vett_Sx(uint8_t row[4], int shift) ;
void shift_rows(uint8_t state[4][4]) ;
void printMatrix(uint8_t matrix[4][4]) ;


#endif
