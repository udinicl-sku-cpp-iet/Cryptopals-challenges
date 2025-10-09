# Variabili
CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = aes_encrypt
SRC = aes_encrypt.c aes.c
OBJ = $(SRC:.c=.o)

# Regola per il target finale
$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

# Regola per i file oggetto
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Regola per pulire i file generati
.PHONY: clean
clean:
	rm -f $(OBJ) $(TARGET)

# Regola per ricompilare tutto
.PHONY: all
all: clean $(TARGET)
