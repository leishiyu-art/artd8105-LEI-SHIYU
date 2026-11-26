/*
  Polyrhythm Loom - sensor test
  Arduino UNO R4 WiFi

  DS18B20 signal -> D2
  Light analog   -> A2
  Button         -> D7 and GND

  This test sends CSV to Serial Monitor.
  It does NOT save to SD card.
*/

#include <OneWire.h>
#include <DallasTemperature.h>

const int TEMP_PIN = 2;
const int LIGHT_PIN = A2;
const int BUTTON_PIN = 7;

const unsigned long SAMPLE_INTERVAL_MS = 10000;
const unsigned long TEMP_CONVERSION_MS = 750;
const unsigned long DEBOUNCE_MS = 40;

OneWire oneWire(TEMP_PIN);
DallasTemperature temperatureSensor(&oneWire);

unsigned long sessionStart = 0;
unsigned long lastSample = 0;
unsigned long conversionStart = 0;

bool conversionPending = false;
float latestTemperature = DEVICE_DISCONNECTED_C;
bool temperatureValid = false;

bool previousRawButton = HIGH;
bool stableButton = HIGH;
unsigned long buttonChangedAt = 0;
unsigned int eventNumber = 0;

void startTemperatureConversion(unsigned long now) {
  temperatureSensor.requestTemperatures();
  conversionStart = now;
  conversionPending = true;
}

void printRow(const char* type, unsigned long elapsedMs, int eventId) {
  Serial.print(type);
  Serial.print(",");
  Serial.print(elapsedMs);
  Serial.print(",");

  if (temperatureValid) {
    Serial.print(latestTemperature, 2);
  }

  Serial.print(",");
  Serial.print(analogRead(LIGHT_PIN));
  Serial.print(",");

  if (eventId > 0) {
    Serial.print(eventId);
  }

  Serial.println();
}

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  temperatureSensor.begin();
  temperatureSensor.setResolution(12);
  temperatureSensor.setWaitForConversion(false);

  sessionStart = millis();
  lastSample = sessionStart;
  buttonChangedAt = sessionStart;

  Serial.println("type,elapsed_ms,temperature_c,light_raw,event_id");

  startTemperatureConversion(sessionStart);
}

void loop() {
  unsigned long now = millis();

  // Read the last completed temperature conversion.
  if (conversionPending &&
      now - conversionStart >= TEMP_CONVERSION_MS) {

    float value = temperatureSensor.getTempCByIndex(0);

    if (value != DEVICE_DISCONNECTED_C &&
        value >= -55.0 && value <= 125.0) {
      latestTemperature = value;
      temperatureValid = true;
    } else {
      temperatureValid = false;
    }

    conversionPending = false;
  }

  // Debounce a normally-open button wired between D7 and GND.
  bool rawButton = digitalRead(BUTTON_PIN);

  if (rawButton != previousRawButton) {
    previousRawButton = rawButton;
    buttonChangedAt = now;
  }

  if ((now - buttonChangedAt >= DEBOUNCE_MS) &&
      rawButton != stableButton) {

    stableButton = rawButton;

    if (stableButton == LOW) {
      eventNumber++;
      printRow("event", now - sessionStart, eventNumber);
    }
  }

  // One sample approximately every 10 seconds.
  if (now - lastSample >= SAMPLE_INTERVAL_MS) {
    lastSample = now;

    printRow("sample", now - sessionStart, 0);

    if (!conversionPending) {
      startTemperatureConversion(now);
    }
  }
}
