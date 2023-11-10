#include <PDM.h>
#include "rain_detector.h"

Eloquent::ML::Port::LogisticRegression clf;

#define SAMPLES 16000
#define SAMPLING_FREQUENCY 16000

short sampleBuffer[SAMPLES];
volatile int samplesRead;

void onPDMdata(void);

void setup() 
  {
    Serial.begin(115200);
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
        float double_array[samplesRead];
        for (int i = 0; i < samplesRead; ++i) 
          {double_array[i] = static_cast<float>(sampleBuffer[i]);}
        int y_pred = clf.predict(double_array);
        Serial.println(y_pred);
        samplesRead = 0;
    }
    delay(100);
  }

void onPDMdata() 
  {
    int bytesAvailable = PDM.available();
    PDM.read(sampleBuffer, bytesAvailable);
    samplesRead = bytesAvailable / 2;
  }