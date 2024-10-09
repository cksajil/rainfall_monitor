#define DATA_RATE_UP_DOWN 2 // Spreading factor (DR0 - DR5)
#define TX_POWER 20         // power option: 2, 5, 8, 11, 14 and 20
#define SESSION_PORT 1      // Port session

// AUXILIARY LIBRARIES

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <wiringPi.h>
#include <lmic.h>
#include <hal.h>
#include <local_hal.h>

// VARIABLES AND DEFINITIONS
// Module RFM95 pin mapping
#define RFM95_PIN_NSS 6
#define RFM95_PIN_RST 0
#define RFM95_PIN_D0 4
#define RFM95_PIN_D1 5
#define DATA_SENT_LED 25

// Dummy definitions to satisfy linker
void os_getArtEui(u1_t *buf) {}
void os_getDevEui(u1_t *buf) {}
void os_getDevKey(u1_t *buf) {}

// Convert u4_t in u1_t(array)
#define msbf4_read(p) (u4_t)((u4_t)(p)[0] << 24 | (u4_t)(p)[1] << 16 | (p)[2] << 8 | (p)[3])

static osjob_t sendjob;

int useLeds = 1; // Default to using LEDs

// Pin mapping
lmic_pinmap pins =
    {
        .nss = RFM95_PIN_NSS,
        .rxtx = UNUSED_PIN,                              // Not connected on RFM92/RFM95
        .rst = RFM95_PIN_RST,                            // Needed on RFM92/RFM95
        .dio = {RFM95_PIN_D0, RFM95_PIN_D1, UNUSED_PIN}, // D0, D1, D2(Not used)
};

void onEvent(ev_t ev)
{
  switch (ev)
  {
  // scheduled data sent (optionally data received)
  // note: this includes the receive window!
  case EV_TXCOMPLETE:

    // use this event to keep track of actual transmissions
    fprintf(stdout, "Event EV_TXCOMPLETE, time: %d\n", millis() / 1000);

    // Check ACK
    if (LMIC.txrxFlags & TXRX_ACK)
      fprintf(stdout, "Received ACK!\n");
    else if (LMIC.txrxFlags & TXRX_NACK)
      fprintf(stdout, "No ACK received!\n");

    // Check DOWN
    if (LMIC.dataLen)
    {
      fprintf(stdout, "RSSI: ");
      fprintf(stdout, "%ld", LMIC.rssi - 96);
      fprintf(stdout, " dBm\n");

      fprintf(stdout, "SNR: ");
      fprintf(stdout, "%ld", LMIC.snr * 0.25);
      fprintf(stdout, " dB\n");

      fprintf(stdout, "Data Received!\n");
      for (int i = 0; i < LMIC.dataLen; i++)
      {
        fprintf(stdout, "0x%02x ", LMIC.frame[LMIC.dataBeg + i]);
      }
      fprintf(stdout, "\n");
    }

    // Turn off the DATA_SENT_LED after data is sent if LEDs are enabled
    if (useLeds)
      digitalWrite(DATA_SENT_LED, LOW);
    LMIC_reset();
    exit(0); // Exit the program after data is sent
    break;
  default:
    fprintf(stdout, "Unknown event\n");
    break;
  }
}

static void do_send(osjob_t *j, float rain, float solar_V, float battery_V, float solar_I, float battery_I)
{
  time_t t = time(NULL);
  fprintf(stdout, "[%x] (%ld) %s\n", hal_ticks(), t, ctime(&t));

  // Show TX channel (channel numbers are local to LMIC)
  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND)
  {
    fprintf(stdout, "OP_TXRXPEND, not sending");
  }
  else
  {
    // Convert floats to fixed-point integer representations (multiplied by 100)
    int int_rain = (int)(rain * 100);
    int int_solar_V = (int)(solar_V * 100);
    int int_battery_V = (int)(battery_V * 100);
    int int_solar_I = (int)(solar_I * 100);
    int int_battery_I = (int)(battery_I * 100);

    // Prepare upstream data transmission at the next possible time.
    unsigned char buf[10]; // 5 values, 2 bytes each = 10 bytes total
    buf[0] = (int_rain >> 8) & 0xFF;
    buf[1] = int_rain & 0xFF;
    buf[2] = (int_solar_V >> 8) & 0xFF;
    buf[3] = int_solar_V & 0xFF;
    buf[4] = (int_battery_V >> 8) & 0xFF;
    buf[5] = int_battery_V & 0xFF;
    buf[6] = (int_solar_I >> 8) & 0xFF;
    buf[7] = int_solar_I & 0xFF;
    buf[8] = (int_battery_I >> 8) & 0xFF;
    buf[9] = int_battery_I & 0xFF;

    LMIC_setTxData2(1, buf, sizeof(buf), 0); // Send all 10 bytes
  }

  // Blink LED to indicate end of transmission attempt if LEDs are enabled
  if (useLeds)
    digitalWrite(DATA_SENT_LED, HIGH);
}

void setup(u1_t *DevAddr, u1_t *Nwkskey, u1_t *Appskey, float rain, float solar_V, float battery_V, float solar_I, float battery_I)
{
  // wiringPi init
  wiringPiSetup();

  // LMIC init
  os_init();

  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();

  // Set static session parameters. Instead of dynamically establishing a session
  // by joining the network, precomputed session parameters are be provided.
  LMIC_setSession(SESSION_PORT, msbf4_read((u1_t *)DevAddr), Nwkskey, Appskey);

  // Multi channel IN865 (CH0-CH7)
  // First, disable channels 8-72
  for (int channel = 8; channel < 72; ++channel)
    LMIC_disableChannel(channel);
  // This means only Indian channels 0-7 are up

  // Disable data rate adaptation
  LMIC_setAdrMode(0);

  // Disable link check validation
  LMIC_setLinkCheckMode(0);

  // Disable beacon tracking
  LMIC_disableTracking();

  // Stop listening for downstream data (periodical reception)
  LMIC_stopPingable();

  // TTN RX2 window.
  LMIC.dn2Dr = 8; // DR8

  // Set data rate and transmit power (note: txpow seems to be ignored by the library)
  LMIC_setDrTxpow(DATA_RATE_UP_DOWN, TX_POWER);

  // Set pin direction if LEDs are enabled
  if (useLeds)
  {
    pinMode(DATA_SENT_LED, OUTPUT);
  }

  // Send data once, passing all the float values
  do_send(&sendjob, rain, solar_V, battery_V, solar_I, battery_I);
}

int main(int argc, char *argv[])
{
  if (argc != 10)
  {
    fprintf(stderr, "Usage: %s <DevAddr> <Nwkskey> <Appskey> <Rain> <solar_V> <battery_V> <solar_I> <battery_I> <UseLeds>\n", argv[0]);
    exit(1);
  }

  u1_t DevAddr[4];
  u1_t Nwkskey[16];
  u1_t Appskey[16];
  float rain, solar_V, battery_V, solar_I, battery_I;

  sscanf(argv[1], "%2hhx%2hhx%2hhx%2hhx", &DevAddr[0], &DevAddr[1], &DevAddr[2], &DevAddr[3]);
  for (int i = 0; i < 16; i++)
    sscanf(&argv[2][i * 2], "%2hhx", &Nwkskey[i]);
  for (int i = 0; i < 16; i++)
    sscanf(&argv[3][i * 2], "%2hhx", &Appskey[i]);
  sscanf(argv[4], "%f", &rain);
  sscanf(argv[5], "%f", &solar_V);
  sscanf(argv[6], "%f", &battery_V);
  sscanf(argv[7], "%f", &solar_I);
  sscanf(argv[8], "%f", &battery_I);
  sscanf(argv[9], "%d", &useLeds);

  setup(DevAddr, Nwkskey, Appskey, rain, solar_V, battery_V, solar_I, battery_I);

  // Run the loop once
  os_runloop();

  return 0;
}

// TTN decode payload
/*
function Decode(fPort, bytes, variables) {
  var decoded = {};
  decoded.rain = ((bytes[0] << 8) | bytes[1]) / 100.0;
  decoded.val1 = ((bytes[2] << 8) | bytes[3]) / 100.0;
  decoded.val2 = ((bytes[4] << 8) | bytes[5]) / 100.0;
  decoded.val3 = ((bytes[6] << 8) | bytes[7]) / 100.0;
  decoded.val4 = ((bytes[8] << 8) | bytes[9]) / 100.0;
  return decoded;
}
*/
