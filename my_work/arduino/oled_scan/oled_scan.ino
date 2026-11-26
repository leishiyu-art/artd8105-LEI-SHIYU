/*
  Finds an OLED on either I2C bus and forces every pixel on.
  Wire  = A4 SDA, A5 SCL, and the SDA/SCL pins beside AREF.
  Wire1 = the Qwiic socket.
*/

#include <Wire.h>
#include <string.h>

static const uint8_t ADDRS[] = {0x3C, 0x3D};

void scan(TwoWire &bus, const char *name) {
  Serial.print("SCAN ");
  Serial.println(name);
  uint8_t found = 0;
  for (uint8_t addr = 1; addr < 127; addr++) {
    bus.beginTransmission(addr);
    uint8_t err = bus.endTransmission();
    if (err == 0) {
      found++;
      Serial.print("I2C 0x");
      if (addr < 16) Serial.print("0");
      Serial.println(addr, HEX);
    }
  }
  if (found == 0) Serial.println("none");
}

bool command(TwoWire &bus, uint8_t addr, uint8_t c) {
  bus.beginTransmission(addr);
  bus.write((uint8_t)0x00);
  bus.write(c);
  return bus.endTransmission() == 0;
}

void fillRam(TwoWire &bus, uint8_t addr, uint8_t pixel) {
  for (uint8_t page = 0; page < 8; page++) {
    command(bus, addr, (uint8_t)(0xB0 + page));
    command(bus, addr, 0x00);
    command(bus, addr, 0x10);
    for (int col = 0; col < 132; col++) {
      bus.beginTransmission(addr);
      bus.write((uint8_t)0x40);
      bus.write(pixel);
      bus.endTransmission();
    }
  }
}

void wake(TwoWire &bus, uint8_t addr) {
  // Contrast 0x81 0xFF is the highest step this chip has.
  // 0xA6 is normal. 0xA7 is inverse. 0xA5 forces every pixel on
  // and does not use the inverse setting.
  // 0xAD 0x8B is the SH1106 panel supply. 0x8D 0x14 is the SSD1306 one.
  static const uint8_t init[] = {
      0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
      0xAD, 0x8B, 0x8D, 0x14,
      0xA1, 0xC8, 0xDA, 0x12, 0x81, 0xFF, 0xD9, 0x1F, 0xDB, 0x40,
      0x33, 0xAF};
  for (uint8_t c : init) command(bus, addr, c);
}

void showMode(TwoWire &bus, uint8_t addr, const char *mode) {
  Serial.println(mode);
  if (strcmp(mode, "ALL_ON") == 0) {
    command(bus, addr, 0xA6);
    command(bus, addr, 0xA5);
  } else if (strcmp(mode, "INVERT") == 0) {
    fillRam(bus, addr, 0x00);
    command(bus, addr, 0xA4);
    command(bus, addr, 0xA7);
  } else {
    fillRam(bus, addr, 0xFF);
    command(bus, addr, 0xA4);
    command(bus, addr, 0xA6);
  }
  command(bus, addr, 0x81);
  command(bus, addr, 0xFF);
}

void light(TwoWire &bus, const char *name) {
  for (uint8_t addr : ADDRS) {
    bus.beginTransmission(addr);
    if (bus.endTransmission() != 0) continue;
    wake(bus, addr);
    Serial.print(name);
    Serial.print(" 0x");
    if (addr < 16) Serial.print("0");
    Serial.println(addr, HEX);
    showMode(bus, addr, "ALL_ON");
    delay(3000);
    showMode(bus, addr, "INVERT");
    delay(3000);
    showMode(bus, addr, "NORMAL");
    delay(3000);
  }
}

void setup() {
  Serial.begin(115200);
  delay(300);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("BOOT");

  Wire.begin();
  Wire.setClock(100000);
  Serial.println("WIRE_OK");

  Wire1.begin();
  Wire1.setClock(100000);
  Serial.println("WIRE1_OK");
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  Serial.println("OLED_SCAN");
  scan(Wire, "A4_A5");
  scan(Wire1, "QWIIC");
  light(Wire, "A4_A5");
  light(Wire1, "QWIIC");
  Serial.println("SCAN_DONE");
}
