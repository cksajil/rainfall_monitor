// https://github.com/antigones/nano33micRGB/blob/master/Nano33Mic.ino
// https://1littleendian.medium.com/the-late-night-tinkering-projects-10-fun-with-fourier-a72b358229b3
// https://github.com/kosme/arduinoFFT/blob/master/Examples/FFT_01/FFT_01.ino

#include "dnn_model.h"
#include <PDM.h> 
#include <arduinoFFT.h> 

#define SAMPLES 256
#define SAMPLING_FREQUENCY 16000

short sampleBuffer[SAMPLES];
volatile int samplesRead;

unsigned long microseconds;

double vReal[SAMPLES];
double vImag[SAMPLES];

void onPDMdata(void);

const int ledPin = 22;
const int ledPin2 = 23;
const int ledPin3 = 24;

const uint8_t amplitude = 100;

arduinoFFT FFT = arduinoFFT();

#define SCL_INDEX 0x00
#define SCL_TIME 0x01
#define SCL_FREQUENCY 0x02

void setup() 

{
    Serial.begin(115200);
    while (!Serial) {}

    while (!dnn_model.begin()) 
        {
            Serial.print("Error in NN initialization: ");
            Serial.println(dnn_model.getErrorMessage());
        }

    PDM.onReceive(onPDMdata);
    PDM.setBufferSize(SAMPLES);

    if (!PDM.begin(1, 16000))
        {
            Serial.println("Failed to start PDM!");
            while (1);
        }

    pinMode(ledPin, OUTPUT);
    pinMode(ledPin2 , OUTPUT);
    pinMode(ledPin3, OUTPUT);

    digitalWrite(ledPin, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, HIGH);
}


void lightOne() 
    {
        digitalWrite(ledPin, LOW);
        digitalWrite(ledPin2, HIGH);
        digitalWrite(ledPin3, HIGH);
    }
void lightTwo() 
    {
        digitalWrite(ledPin, HIGH);
        digitalWrite(ledPin2, LOW);
        digitalWrite(ledPin3, HIGH);
    }
void lightThree() 
    {
        digitalWrite(ledPin, HIGH);
        digitalWrite(ledPin2, HIGH);
        digitalWrite(ledPin3, LOW);
    }

void PrintVector(double *vData, uint16_t bufferSize, uint8_t scaleType)
{
  for (uint16_t i = 0; i < bufferSize; i++)
  {
    double abscissa;
    /* Print abscissa value */
    switch (scaleType)
    {
      case SCL_INDEX:
        abscissa = (i * 1.0);
	break;
      case SCL_TIME:
        abscissa = ((i * 1.0) /  SAMPLING_FREQUENCY);
	break;
      case SCL_FREQUENCY:
        abscissa = ((i * 1.0 * SAMPLING_FREQUENCY) / SAMPLES);
	break;
    }
    Serial.print(abscissa, 6);
    if(scaleType==SCL_FREQUENCY)
      Serial.print("Hz");
    Serial.print(" ");
    Serial.println(vData[i], 4);
  }
  Serial.println();
}



void loop() 
{
    if (samplesRead) 
        {
            for (int i = 0; i < SAMPLES; i++) 
                {
                    vReal[i] = sampleBuffer[i];
                    vImag[i] = 0;
                }
            FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
            FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
            FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
            Serial.println("Computed magnitudes:");
            PrintVector(vReal, (SAMPLES >> 1), SCL_FREQUENCY);
            // float y_pred = dnn_model.predict(magnitude);
            // Serial.println("Predicted output:");
            // Serial.println(y_pred);
            delay(100);
    }
}

void onPDMdata()
    {
        int bytesAvailable = PDM.available();
        PDM.read(sampleBuffer, bytesAvailable);
        samplesRead = bytesAvailable / 2;
    }