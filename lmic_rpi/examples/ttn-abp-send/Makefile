CFLAGS=-I../../lmic
LDFLAGS=-lwiringPi

ttn-abp-send: ttn-abp-send.cpp
	cd ../../lmic && $(MAKE)
	$(CC) $(CFLAGS) -o ttn-abp-send ttn-abp-send.cpp ../../lmic/*.o $(LDFLAGS)

all: ttn-abp-send

run: ./ttn-abp-send

.PHONY: clean

clean:
	rm -f *.o ttn-abp-send
