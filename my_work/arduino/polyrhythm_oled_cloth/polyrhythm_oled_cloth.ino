/*
  Polyrhythm Loom — field cloth on the OLED
  Arduino UNO R4 WiFi

  DS18B20 signal -> D2
  Light analog   -> A2
  Button         -> D7 and GND
  OLED SH1106    -> SDA A4, SCL A5, GND, and the voltage printed on the module

  Serial stays CSV only, 115200, one sample row every 10 seconds.
  The cloth on the glass weaves faster than the log. It does NOT save to SD.
*/

#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

const int TEMP_PIN = 2;
const int LIGHT_PIN = A2;
const int BUTTON_PIN = 7;

const unsigned long SAMPLE_INTERVAL_MS = 10000;
const unsigned long WEAVE_INTERVAL_MS = 1000;
const unsigned long TEMP_CONVERSION_MS = 750;
const unsigned long DEBOUNCE_MS = 40;
const unsigned long DRAW_INTERVAL_MS = 80;

const int W = 128;
const int H = 64;
const int TEXT_H = 8;
const int CLOTH_ROWS = H - TEXT_H - 1;
const int SEL = 6;
const int KNOT_SPAN = 7;
const int KNOT_X = 18; // center sits on a warp, inward from the selvedge

// About 36 raw counts either side of the recent light level
// moves the weft from sparse to dense.
const float LIGHT_SWING = 36.0f;

Adafruit_SH1106G display(W, H, &Wire, -1);

OneWire oneWire(TEMP_PIN);
DallasTemperature temperatureSensor(&oneWire);

unsigned long sessionStart = 0;
unsigned long lastSample = 0;
unsigned long lastWeave = 0;
unsigned long conversionStart = 0;
unsigned long lastDraw = 0;

bool conversionPending = false;
float latestTemperature = DEVICE_DISCONNECTED_C;
bool temperatureValid = false;

bool previousRawButton = HIGH;
bool stableButton = HIGH;
unsigned long buttonChangedAt = 0;
unsigned int eventNumber = 0;

bool oledOk = false;
bool liveMark = false;
bool birdFlying = false;
int birdX = 0;
int birdPose = 0;
int birdSteps = 0;
unsigned long lastBird = 0;

float lightCenter = 0;
bool lightReady = false;

struct Row {
  uint8_t bits[16];
  bool mark;
};

Row rows[CLOTH_ROWS];
int rowCount = 0;

uint8_t weaveHash(int x, int y, int salt) {
  uint32_t n = (uint32_t)(x * 374761393 + y * 668265263 + salt * 1442695041);
  n = (n ^ (n >> 13)) * 1274126177u;
  return (uint8_t)(n >> 24);
}

void setBit(Row &row, int x) {
  row.bits[x >> 3] |= (uint8_t)(1 << (x & 7));
}

bool bitOn(const Row &row, int x) {
  return row.bits[x >> 3] & (uint8_t)(1 << (x & 7));
}

float lightAmount(int raw) {
  if (!lightReady) return 0.55f;
  float u = 0.5f + ((float)raw - lightCenter) / LIGHT_SWING;
  if (u < 0.05f) u = 0.05f;
  if (u > 0.95f) u = 0.95f;
  return u;
}

void followLight(int raw) {
  if (!lightReady) {
    lightCenter = raw;
    lightReady = true;
    return;
  }
  lightCenter += ((float)raw - lightCenter) * 0.12f;
}

void fillRow(Row &row, int lightRaw, bool tempOk, bool mark, int ySalt) {
  memset(row.bits, 0, sizeof(row.bits));
  row.mark = mark;
  float amount = lightAmount(lightRaw);
  int salt = tempOk ? (int)(latestTemperature * 8.0f) : 0;
  uint8_t threshold = (uint8_t)(amount * 255.0f);

  for (int s = 0; s < SEL; s++) {
    if (mark) setBit(row, s);
  }

  if (mark) {
    int start = KNOT_X - (KNOT_SPAN / 2);
    for (int i = 0; i < KNOT_SPAN; i++) {
      int x = start + i;
      if (x >= SEL && x < W) setBit(row, x);
    }
  }

  for (int x = 0; x < W - SEL; x++) {
    int px = x + SEL;
    bool warp = (x % 4) == 0;
    bool weft = weaveHash(x + salt, ySalt, salt) < threshold;
    if (warp || weft) setBit(row, px);
  }
}

void rememberRow(int lightRaw, bool mark) {
  int salt = rowCount;
  if (rowCount < CLOTH_ROWS) {
    fillRow(rows[rowCount], lightRaw, temperatureValid, mark, salt);
    rowCount++;
    return;
  }
  for (int i = 0; i < CLOTH_ROWS - 1; i++) rows[i] = rows[i + 1];
  fillRow(rows[CLOTH_ROWS - 1], lightRaw, temperatureValid, mark, salt);
}

void drawLabel(int lightRaw) {
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 0);
  if (temperatureValid) {
    display.print(latestTemperature, 1);
    display.print("C");
  } else {
    display.print("--");
  }
  display.print(" L");
  display.print(lightRaw);
  if (eventNumber > 0) {
    display.print(" #");
    display.print(eventNumber);
  }
}

void drawCloth() {
  setMaxBrightness();
  int liveRaw = analogRead(LIGHT_PIN);
  if (!lightReady) {
    lightCenter = liveRaw;
    lightReady = true;
  }
  Row live;
  fillRow(live, liveRaw, temperatureValid, liveMark, rowCount);

  display.clearDisplay();
  int visible = rowCount < CLOTH_ROWS ? rowCount : CLOTH_ROWS;
  int top = (H - 1) - visible;
  for (int y = TEXT_H; y < top; y++) {
    Row provisional;
    fillRow(provisional, liveRaw, temperatureValid, false, y);
    for (int x = 0; x < W; x++) {
      if (bitOn(provisional, x)) display.drawPixel(x, y, SH110X_WHITE);
    }
  }
  for (int i = 0; i < visible; i++) {
    int y = top + i;
    for (int x = 0; x < W; x++) {
      if (bitOn(rows[i], x)) display.drawPixel(x, y, SH110X_WHITE);
    }
  }
  for (int x = 0; x < W; x++) {
    if (bitOn(live, x)) display.drawPixel(x, H - 1, SH110X_WHITE);
  }
  drawLabel(liveRaw);
  display.display();
}

void startTemperatureConversion(unsigned long now) {
  temperatureSensor.requestTemperatures();
  conversionStart = now;
  conversionPending = true;
}

void printRow(const char *type, unsigned long elapsedMs, int eventId) {
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

const int BIRD_W = 40;
const int BIRD_H = 34;
const int BIRD_STEP = 2;
const int BIRD_X0 = W;
const int BIRD_X1 = -BIRD_W;
const int BIRD_Y0 = H - BIRD_H;
const int BIRD_Y1 = 0;

const uint8_t BIRD_0[] PROGMEM = {
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x20, 0x00, 0x00, 0x00, 0x01, 0xFC, 0x00, 0x00, 0x00, 0x07, 0x07,
  0x20, 0x00, 0x00, 0x7C, 0x01, 0xF0, 0x00, 0x00, 0xE0, 0x01, 0xE0, 0x00,
  0x00, 0xC0, 0x03, 0x80, 0x00, 0x01, 0x80, 0x0F, 0x00, 0x00, 0x01, 0x80,
  0x38, 0x00, 0x00, 0x03, 0x00, 0xE0, 0x00, 0x00, 0x0B, 0x03, 0x80, 0x00,
  0x00, 0x1F, 0xFE, 0x00, 0x00, 0x7C, 0x7F, 0xFF, 0x03, 0xF8, 0x03, 0xFF,
  0xFF, 0xFC, 0x00, 0x00, 0x7F, 0xFF, 0xE0, 0x00, 0x01, 0xFF, 0xFF, 0xC0,
  0x00, 0x1E, 0x0F, 0xFF, 0xC0, 0x00, 0x00, 0x1F, 0xFF, 0xBF, 0x00, 0x00,
  0x38, 0x00, 0x00, 0xE0, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00,
  0x00, 0x00, 0x00, 0xE0, 0x00, 0x00, 0x00, 0x01, 0xC0, 0x00, 0x00, 0x00,
  0x00, 0x80, 0x00, 0x08, 0x00, 0x01, 0xC0, 0x00, 0x1C, 0x00, 0x00, 0xC0,
  0x00, 0x38, 0x00, 0x00, 0xE0, 0x00, 0x70, 0x00, 0x00, 0x70, 0x00, 0xE0,
  0x00, 0x00, 0x38, 0x01, 0xC0, 0x00, 0x00, 0x18, 0x03, 0x80, 0x00, 0x00,
  0x1F, 0xFF, 0x00, 0x00, 0x00, 0x0F, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00,
};
const uint8_t BIRD_1[] PROGMEM = {
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x07, 0xFF, 0xC0, 0x00, 0x00, 0x0F,
  0xFF, 0x80, 0x00, 0x00, 0x3C, 0x0E, 0x00, 0x00, 0x08, 0x70, 0x7C, 0x00,
  0x00, 0x1F, 0xFF, 0xC0, 0x00, 0x7C, 0x7F, 0xFF, 0x03, 0xF8, 0x03, 0xFF,
  0xFF, 0xFC, 0x00, 0x00, 0x7F, 0xFF, 0xE0, 0x00, 0x01, 0xFF, 0xFF, 0xC0,
  0x00, 0x1E, 0x0F, 0xFF, 0xC0, 0x00, 0x00, 0x07, 0xFF, 0xBF, 0x00, 0x00,
  0x06, 0x00, 0x00, 0xE0, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00,
  0x00, 0x00, 0x00, 0x0C, 0x00, 0x10, 0x00, 0x00, 0x0C, 0x00, 0x78, 0x00,
  0x00, 0x0C, 0x00, 0xE0, 0x00, 0x00, 0x0F, 0x03, 0xC0, 0x00, 0x00, 0x01,
  0xC7, 0x00, 0x00, 0x00, 0x00, 0x7E, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00,
};
const uint8_t BIRD_2[] PROGMEM = {
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00,
  0x00, 0x1F, 0xFE, 0x00, 0x00, 0x7C, 0x7F, 0xFF, 0x83, 0xF8, 0x03, 0xFF,
  0xFF, 0xFC, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xC0, 0x01, 0xFF, 0xFF, 0xC3,
  0xC0, 0x1E, 0x0F, 0xFF, 0xC0, 0x40, 0x00, 0x03, 0xFF, 0xBF, 0x00, 0x00,
  0x03, 0x80, 0x07, 0xE0, 0x00, 0x01, 0xC0, 0x0E, 0x00, 0x00, 0x00, 0xC0,
  0x1C, 0x00, 0x00, 0x00, 0xE0, 0x38, 0x00, 0x00, 0x00, 0x7F, 0xF0, 0x00,
  0x00, 0x00, 0x3F, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00,
};
const uint8_t *const BIRD_POSES[] = {BIRD_0, BIRD_1, BIRD_2, BIRD_1};

int birdY() {
  return BIRD_Y0 + (birdX - BIRD_X0) * (BIRD_Y1 - BIRD_Y0) / (BIRD_X1 - BIRD_X0);
}

void startBird() {
  birdX = BIRD_X0;
  birdPose = 0;
  birdSteps = 0;
  birdFlying = true;
  lastBird = millis();
  if (oledOk) drawBird();
}

void drawBird() {
  display.clearDisplay();
  display.drawBitmap(birdX, birdY(), BIRD_POSES[birdPose], BIRD_W, BIRD_H, SH110X_WHITE);
  display.display();
}

bool advanceBird() {
  birdX -= BIRD_STEP;
  birdSteps++;
  if (birdSteps >= 3) {
    birdSteps = 0;
    birdPose = (birdPose + 1) % 4;
  }
  if (birdX < BIRD_X1) {
    birdFlying = false;
    return false;
  }
  drawBird();
  return true;
}

void setMaxBrightness() {
  display.setContrast(255);
}

void forceWhite() {
  // Same sequence that lit this panel indoors. Held so it can be seen in shade.
  Wire.begin();
  static const uint8_t init[] = {
      0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40, 0xAD, 0x8B,
      0xA1, 0xC8, 0xDA, 0x12, 0x81, 0xFF, 0xD9, 0x1F, 0xDB, 0x40,
      0x33, 0xA6, 0x20, 0x10, 0xA4, 0xAF, 0xA5};
  for (uint8_t c : init) {
    Wire.beginTransmission(0x3C);
    Wire.write((uint8_t)0x00);
    Wire.write(c);
    Wire.endTransmission();
  }
  delay(2000);
  Wire.beginTransmission(0x3C);
  Wire.write((uint8_t)0x00);
  Wire.write((uint8_t)0xA4);
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  forceWhite();

  temperatureSensor.begin();
  temperatureSensor.setResolution(12);
  temperatureSensor.setWaitForConversion(false);

  oledOk = display.begin(0x3C, false) || display.begin(0x3D, false);
  digitalWrite(LED_BUILTIN, oledOk ? LOW : HIGH);
  if (oledOk) {
    display.setTextWrap(false);
    setMaxBrightness();
    display.clearDisplay();
    display.display();
  }

  sessionStart = millis();
  lastSample = sessionStart;
  lastWeave = sessionStart;
  lastDraw = sessionStart;
  buttonChangedAt = sessionStart;

  Serial.println("type,elapsed_ms,temperature_c,light_raw,event_id");
  startTemperatureConversion(sessionStart);
}

void loop() {
  unsigned long now = millis();

  if (conversionPending && now - conversionStart >= TEMP_CONVERSION_MS) {
    float value = temperatureSensor.getTempCByIndex(0);
    if (value != DEVICE_DISCONNECTED_C && value >= -55.0 && value <= 125.0) {
      latestTemperature = value;
      temperatureValid = true;
    } else {
      temperatureValid = false;
    }
    conversionPending = false;
    startTemperatureConversion(now);
  }

  bool rawButton = digitalRead(BUTTON_PIN);
  if (rawButton != previousRawButton) {
    previousRawButton = rawButton;
    buttonChangedAt = now;
  }

  if ((now - buttonChangedAt >= DEBOUNCE_MS) && rawButton != stableButton) {
    stableButton = rawButton;
    if (stableButton == LOW) {
      eventNumber++;
      liveMark = true;
      startBird();
      printRow("event", now - sessionStart, eventNumber);
    }
  }

  if (now - lastWeave >= WEAVE_INTERVAL_MS) {
    lastWeave = now;
    int raw = analogRead(LIGHT_PIN);
    followLight(raw);
    rememberRow(raw, liveMark);
    liveMark = false;
  }

  if (now - lastSample >= SAMPLE_INTERVAL_MS) {
    lastSample = now;
    printRow("sample", now - sessionStart, 0);
  }

  if (oledOk && birdFlying && now - lastBird >= 30) {
    lastBird = now;
    if (!advanceBird()) drawCloth();
  } else if (oledOk && !birdFlying && now - lastDraw >= DRAW_INTERVAL_MS) {
    lastDraw = now;
    drawCloth();
  }
}
