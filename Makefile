CC=gcc
CFLAGS=-Wall -Wextra -O2

all: mkd

mkd: src/main.c
	$(CC) $(CFLAGS) -o mkd src/main.c

clean:
	rm -f mkd
