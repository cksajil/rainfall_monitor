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

arduinoFFT FFT = arduinoFFT();

void setup() {
  Serial.begin(115200);
   
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
 
  PDM.onReceive(onPDMdata);
  PDM.setBufferSize(SAMPLES);
  //PDM.setGain(0);
  // setup the I2S audio input for the sample rate with 32-bits per sample
  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
  
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

     for (int i = 0; i < SAMPLES; i++) {
      Serial.println(vReal[i]);
    }
 
  }
}

void onPDMdata()
{
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;
}
