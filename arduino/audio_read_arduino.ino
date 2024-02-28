#include <PDM.h>
#include <arduinoFFT.h>

#define NUM_MEL_FILTERS 64
#define SAMPLES 256
#define SAMPLING_FREQUENCY 8000

short sampleBuffer[SAMPLES];
volatile int samplesRead;
float melFilters[NUM_MEL_FILTERS][SAMPLES / 2];
float melCoefficients[NUM_MEL_FILTERS];

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
        process_audio_segment(sampleBuffer);
        // clear the read count
        samplesRead = 0;
      }
  }



void process_audio_segment(short audio_segment[SAMPLES])
   {
    for (int i = 0; i < samplesRead; i++) 
      {Serial.println(audio_segment[i]);}
   }


void onPDMdata() 
  {
    int bytesAvailable = PDM.available();
    PDM.read(sampleBuffer, bytesAvailable);
    samplesRead = bytesAvailable / 2;
  }
