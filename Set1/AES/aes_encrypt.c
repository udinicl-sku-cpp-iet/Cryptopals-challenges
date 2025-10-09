#include <stdio.h>
#include <stdint.h>
#include "aes.h"


int main() {
    // Esempio di matrice di stato 4x4
    uint8_t state[4][4] = {
        {0xea, 0x04, 0x65, 0x85},
        {0x83, 0x45, 0x5d, 0x96},
        {0x5c, 0x33, 0x98, 0xb0},
        {0xf0, 0x2d, 0xad, 0xc5}
    };

    // Stampa la matrice originale
    printf("Original State:\n");
    printMatrix(state);

    // Applica la funzione SubBytes
    sub_bytes(state);

    // Stampa la matrice dopo SubBytes
    printf("\nState After SubBytes:\n");
    printMatrix(state);

	shift_rows(state);

	// Stampa la matrice dopo ShiftRows
    printf("\nState After ShiftRows:\n");
    printMatrix(state);

	mix_columns(state);

	// Stampa la matrice dopo MixColumns
    printf("\nState After MixColumns:\n");
    printMatrix(state);

	int n_of_rounds;
	int keysize = 128;
	char carattere = 65;
	uint8_t numero=(uint8_t)carattere;
	int bo=-1;

	printf("%X",bo);

	if (keysize = 128){
		n_of_rounds=10;
	}
	if (keysize = 192){
		n_of_rounds=12;
	}
	if (keysize = 256){
		n_of_rounds=14;
	}

    return 0;
}
