#include <PDM.h>
#include "mbed.h"

#define SAMPLES 256
#define SAMPLE_RATE 16000
#define AUDIO_LENGTH_SEC 5
#define AUDIO_LENGTH_SAMPLES (SAMPLE_RATE * AUDIO_LENGTH_SEC)

short sampleBuffer[SAMPLES];
volatile int samplesRead;
void onPDMdata(void);
static const char CHANNELS = 1;

mbed::Ticker timer;

struct Buffer
{
  int32_t cur_idx{0};
  bool is_ready{false};
  int16_t data[AUDIO_LENGTH_SAMPLES];
};

volatile Buffer buffer;

void print_raw_audio()
{
  for (int i = 0; i < AUDIO_LENGTH_SAMPLES; ++i)
  {
    Serial.println((int32_t)buffer.data[i]);
  }
}

void timer_ISR()
{
  if (buffer.cur_idx < AUDIO_LENGTH_SAMPLES)
  {
    for (int i = 0; i < samplesRead; i++)
    {
      // Serial.println(sampleBuffer[i]);
      int16_t v = (int16_t)(sampleBuffer[i]);

      // Get current buffer index
      int32_t ix_buffer = buffer.cur_idx;

      // Store the sample in the audio buffer
      buffer.data[ix_buffer] = (int16_t)v;

      // Increment buffer index
      buffer.cur_idx++;
    }
    samplesRead = 0;
  }
  else
  {
    buffer.is_ready = true;
  }
}

void setup()
{

  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

  PDM.onReceive(onPDMdata);
  PDM.setGain(60);

  if (!PDM.begin(CHANNELS, SAMPLE_RATE))
  {
    Serial.println("Failed to start PDM!");
  }
}

void loop()

{
  // delay(800);

  // Reset audio buffer
  buffer.cur_idx = 0;
  buffer.is_ready = false;
  digitalWrite(LED_BUILTIN, HIGH);

  constexpr uint32_t sr_us = 1000000 / SAMPLE_RATE;
  timer.attach_us(&timer_ISR, sr_us);

  while (!buffer.is_ready)
    ;

  timer.detach();

  digitalWrite(LED_BUILTIN, LOW);

  print_raw_audio();
}

void onPDMdata()
{
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;
}