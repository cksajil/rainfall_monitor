#include "dnn_model.h"
#include <PDM.h> 
#include <arduinoFFT.h> 

#define SAMPLES 16000
#define SAMPLING_FREQUENCY 16000

short sampleBuffer[SAMPLES];
volatile int samplesRead;
double vReal[SAMPLES];
double vImag[SAMPLES];
void onPDMdata(void);
const int ledPin = 22; //red
const int ledPin2 = 23; //green
const int ledPin3 = 24; //blue

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

void onPDMdata()
    {
        int bytesAvailable = PDM.available();
        PDM.read(sampleBuffer, bytesAvailable);
        samplesRead = bytesAvailable / 2;
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
            short magnitude = FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
            float y_pred = dnn_model.predict(magnitude);
            Serial.println("Predicted output:");
            Serial.println(y_pred);
            delay(100);
    }
}