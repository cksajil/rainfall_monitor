#include <PDM.h>
#include <arduinoFFT.h>
// #include "dnn_model.h"

#define SAMPLES 16
#define SAMPLING_FREQUENCY 16000

short sampleBuffer[SAMPLES];
volatile int samplesRead;

double vReal[SAMPLES];
double vImag[SAMPLES];

void onPDMdata(void);

arduinoFFT FFT = arduinoFFT();

void setup() 
  {
    Serial.begin(9600);
    while (!Serial){};

    // while (!dnn_model.begin()) 
    //     {
    //         Serial.print("Error in NN initialization: ");
    //         Serial.println(dnn_model.getErrorMessage());
    //     }

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
          // Serial.println(double_array[i]);
          vReal[i] = double_array[i];
          vImag[i] = 0;    
        }
      FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
      FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
      FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

      for (int i = 0; i < samplesRead; i++) 
        { 
          Serial.println(vReal[i]);
        }
      // float y_pred = dnn_model.predict(vReal);
      // Serial.println("Predicted output:");
      // Serial.println(y_pred);
      
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