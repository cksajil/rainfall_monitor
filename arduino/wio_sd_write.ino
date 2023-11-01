#include <Seeed_FS.h>
#include "DateTime.h"
#include "RTC_SAMD51.h"

#define SERIAL Serial
#ifdef USESPIFLASH
#define DEV SPIFLASH
#include "SFUD/Seeed_SFUD.h"
#else
#define DEV SD
#include "SD/Seeed_SD.h"
#endif 

#ifdef _SAMD21_
#define SDCARD_SS_PIN 1
#define SDCARD_SPI SPI
#endif 

RTC_SAMD51 rtc;

void setup() {
    Serial.begin(2000000);
    rtc.begin();
    
    pinMode(WIO_MIC, INPUT);
    pinMode(5, OUTPUT);
    digitalWrite(5, HIGH);
    
    while (!SERIAL) {};
    
#ifdef SFUD_USING_QSPI
    while (!DEV.begin(104000000UL)) 
    {
        SERIAL.println("Card Mount Failed");
        return;
    }
#else
    while (!DEV.begin(SDCARD_SS_PIN,SDCARD_SPI,4000000UL)) 
    {
        SERIAL.println("Card Mount Failed");
        return;
    }
#endif 

    SERIAL.println("initialization done.");

    File RootWrite = DEV.open("/readings.txt", "w");

    if (RootWrite) {
        SERIAL.print("Writing to the file...");

        for (unsigned int i=0; i<64000; i++)
        { 
          DateTime now = rtc.now();
          int val = analogRead(WIO_MIC);
          
//          RootWrite.print(now.hour(), DEC);
//          RootWrite.print(':');
//          
//          RootWrite.print(now.minute(), DEC);
//          RootWrite.print(':');
          
//          RootWrite.print(now.second(), DEC);
//          RootWrite.print(',');
//          
          RootWrite.println(val);
          
        }
     
   
        RootWrite.close();
        SERIAL.println("done.");
        
    } else 
    {
        SERIAL.println("error opening hello.txt");
    }


    
    // re-open the file for reading:
    File RootRead= DEV.open("/readings.txt");
    if (RootRead) {
        SERIAL.println("Sample readings are as follows");

        // read from the file until there's nothing else in it:
        while (RootRead.available()) 
        {
            SERIAL.write(RootRead.read());
        }
     
        RootRead.close();
    } else 
    {
        SERIAL.println("error opening readings.txt");
    }
}

void loop() {
  //do
  }

