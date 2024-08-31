#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <wiringPi.h>
#include <lmic.h>
#include <hal.h>
#include <local_hal.h>

#define DATA_RATE_UP_DOWN 2 // Spreading factor (DR0 - DR5)
#define TX_POWER 20         // Power option: 2, 5, 8, 11, 14, and 20
#define SESSION_PORT 1      // Port session

// MODULE RFM95 PIN MAPPING
#define RFM95_PIN_NSS 6
#define RFM95_PIN_RST 0
#define RFM95_PIN_D0 4
#define RFM95_PIN_D1 5
#define DATA_SENT_LED 25

// Dummy definitions to satisfy linker
void os_getArtEui(u1_t *buf) {}
void os_getDevEui(u1_t *buf) {}
void os_getDevKey(u1_t *buf) {}

// Convert u4_t in u1_t (array)
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
  case EV_TXCOMPLETE:
    // Use this event to keep track of actual transmissions
    fprintf(stdout, "Event EV_TXCOMPLETE, time: %d\n", millis() / 1000);

    // Check ACK
    if (LMIC.txrxFlags & TXRX_ACK)
      fprintf(stdout, "Received ACK!\n");
    else if (LMIC.txrxFlags & TXRX_NACK)
      fprintf(stdout, "No ACK received!\n");

    // Check DOWN
    if (LMIC.dataLen)
    {
      fprintf(stdout, "RSSI: %d dBm\n", LMIC.rssi - 96);
      fprintf(stdout, "SNR: %f dB\n", LMIC.snr * 0.25);

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

static void do_send(osjob_t *j, float rain, float battery_voltage, float battery_current, float solar_voltage, float solar_current)
{
  time_t t = time(NULL);
  fprintf(stdout, "[%x] (%ld) %s\n", hal_ticks(), t, ctime(&t));

  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND)
  {
    fprintf(stdout, "OP_TXRXPEND, not sending");
  }
  else
  {
    // Prepare upstream data transmission at the next possible time.
    unsigned char buf[20];

    // Convert each float value to a fixed-point integer representation (4 bytes each)
    float values[5] = {rain, battery_voltage, battery_current, solar_voltage, solar_current};

    for (int i = 0; i < 5; i++)
    {
      int int_val = (int)(values[i] * 100); // 2 decimal places
      buf[i * 4 + 0] = (int_val >> 24) & 0xFF;
      buf[i * 4 + 1] = (int_val >> 16) & 0xFF;
      buf[i * 4 + 2] = (int_val >> 8) & 0xFF;
      buf[i * 4 + 3] = int_val & 0xFF;
    }

    LMIC_setTxData2(SESSION_PORT, buf, sizeof(buf), 0);
  }

  // Blink LED to indicate end of transmission attempt if LEDs are enabled
  if (useLeds)
    digitalWrite(DATA_SENT_LED, HIGH);
}

void setup(u1_t *DevAddr, u1_t *Nwkskey, u1_t *Appskey, float rain, float battery_voltage, float battery_current, float solar_voltage, float solar_current)
{
  // wiringPi init
  wiringPiSetup();

  // LMIC init
  os_init();

  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();

  // Set static session parameters. Instead of dynamically establishing a session
  // by joining the network, precomputed session parameters are provided.
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

  // Send data once
  do_send(&sendjob, rain, battery_voltage, battery_current, solar_voltage, solar_current);
}

int main(int argc, char *argv[])
{
  if (argc != 10)
  {
    fprintf(stderr, "Usage: %s <DevAddr> <Nwkskey> <Appskey> <Rain> <BatteryVoltage> <BatteryCurrent> <SolarVoltage> <SolarCurrent> <UseLeds>\n", argv[0]);
    return EXIT_FAILURE;
  }

  u1_t DevAddr[4];
  u1_t Nwkskey[16];
  u1_t Appskey[16];
  float rain, battery_voltage, battery_current, solar_voltage, solar_current;
  int useLeds;

  if (sscanf(argv[1], "%2hhx%2hhx%2hhx%2hhx", &DevAddr[0], &DevAddr[1], &DevAddr[2], &DevAddr[3]) != 4 ||
      sscanf(argv[4], "%f", &rain) != 1 ||
      sscanf(argv[5], "%f", &battery_voltage) != 1 ||
      sscanf(argv[6], "%f", &battery_current) != 1 ||
      sscanf(argv[7], "%f", &solar_voltage) != 1 ||
      sscanf(argv[8], "%f", &solar_current) != 1 ||
      sscanf(argv[9], "%d", &useLeds) != 1)
  {
    fprintf(stderr, "Error parsing arguments\n");
    return EXIT_FAILURE;
  }

  for (int i = 0; i < 16; i++)
  {
    if (sscanf(&argv[2][i * 2], "%2hhx", &Nwkskey[i]) != 1 ||
        sscanf(&argv[3][i * 2], "%2hhx", &Appskey[i]) != 1)
    {
      fprintf(stderr, "Error parsing keys\n");
      return EXIT_FAILURE;
    }
  }

  setup(DevAddr, Nwkskey, Appskey, rain, battery_voltage, battery_current, solar_voltage, solar_current);

  // Run the loop once
  os_runloop();

  return EXIT_SUCCESS;
}

// function Decode(fPort, bytes, variables) {
//     var decoded = {};

//     if (bytes.length === 20) {
//         // Extract and decode each value from the byte array
//         decoded.rain = ((bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3]) / 100.0);
//         decoded.battery_voltage = ((bytes[4] << 24 | bytes[5] << 16 | bytes[6] << 8 | bytes[7]) / 100.0);
//         decoded.battery_current = ((bytes[8] << 24 | bytes[9] << 16 | bytes[10] << 8 | bytes[11]) / 100.0);
//         decoded.solar_voltage = ((bytes[12] << 24 | bytes[13] << 16 | bytes[14] << 8 | bytes[15]) / 100.0);
//         decoded.solar_current = ((bytes[16] << 24 | bytes[17] << 16 | bytes[18] << 8 | bytes[19]) / 100.0);
//     }

//     return decoded;
// }
