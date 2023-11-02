#include <math.h>
#include <SPI.h>
#include <Seeed_FS.h>
#include "SD/Seeed_SD.h"
#include "RTC_SAMD51.h"
#include "DateTime.h"


RTC_SAMD51 rtc;
#define SERIAL Serial
#define DEV SD


#ifdef _SAMD21_
#define SDCARD_SS_PIN 1
#define SDCARD_SPI SPI
#endif 


void setup() 
  {
    Serial.begin(9600);
    analogReadResolution(16);
        
    rtc.begin();

    pinMode(WIO_KEY_A, INPUT);
    pinMode(WIO_KEY_B, INPUT);
    
    pinMode(WIO_MIC, INPUT);
    pinMode(5, OUTPUT);

    

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
    
   }
    
void loop() 

{
  
  
  if (digitalRead(WIO_KEY_A)==LOW)
        
        { 
          Serial.println("Waiting in idle time");
          delay(10000);
          Serial.println("Recording key pressed");
          digitalWrite(5, HIGH);
          while (!SERIAL) {};
    
          File RootWrite = DEV.open("readings.txt", "w");
    
          if (RootWrite) 
              {
                SERIAL.println("Writing to the file after button A pressed...");

                for (unsigned int i=0; i<64000; i++)
                      { 
//                          DateTime now = rtc.now();
                          int val = analogRead(WIO_MIC);
                          
//                          RootWrite.print(now.hour(), DEC);
//                          RootWrite.print(':');
//                         
//                          RootWrite.print(now.minute(), DEC);
//                          RootWrite.print(':');
//                          
//                          RootWrite.print(now.second(), DEC);
//                          RootWrite.print(',');
                        
                          RootWrite.println(val);
                      }
     
   
                RootWrite.close();
                SERIAL.println("recording completed.");
        
               } 
    
            else 
                {
                    SERIAL.println("error opening readings.txt");
                }
    
        delay(1000);
        }

        else if (digitalRead(WIO_KEY_B) == LOW) 
            {
                Serial.println("Button B pressed, displaying contents of file recorded");
                digitalWrite(5, LOW);
                
                File RootRead= DEV.open("readings.txt");
                
                if (RootRead) 
                    {
                        SERIAL.println("Sample readings are as follows");
                    
                        while (RootRead.available()) 
                            {
                              SERIAL.write(RootRead.read());
                            }
                 
                        RootRead.close();
                    } 
                else 
                    {
                    SERIAL.println("error opening readings.txt");
                    }

             delay(1000);   
            }
 }

    