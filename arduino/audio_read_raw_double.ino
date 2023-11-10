#include <PDM.h>
#include <arduinoFFT.h>

#define SAMPLES 1024
#define SAMPLING_FREQUENCY 16000

short sampleBuffer[SAMPLES];
volatile int samplesRead;

void onPDMdata(void);

void setup() 
  {
    Serial.begin(9600);
    while (!Serial){};

    PDM.onReceive(onPDMdata);
    PDM.setBufferSize(SAMPLES);
    // optionally set the gain, defaults to 20
    // PDM.setGain(30);
    if (!PDM.begin(1, 16000)) 
      {
        Serial.println("Failed to start PDM!");
        while (1);
      }
  }



void loop() 
  {
  if (samplesRead) 
    { 
      double double_array[samplesRead];
      for (int i = 0; i < samplesRead; ++i) 
        {double_array[i] = static_cast<double>(sampleBuffer[i]);}
      for (int i = 0; i < samplesRead; i++) 
        { 
          Serial.println(double_array[i]);
 
        }
      
      // clear the read count
      samplesRead = 0;
    }
  }

void onPDMdata() 
  {
    int bytesAvailable = PDM.available();
    PDM.read(sampleBuffer, bytesAvailable);
    samplesRead = bytesAvailable / 2;
  }