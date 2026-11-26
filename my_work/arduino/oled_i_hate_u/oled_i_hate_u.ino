/*
  Shows "I hate U" on the SH1106.
  Arduino UNO R4 WiFi
  OLED -> SDA A4, SCL A5, GND, VCC as printed on the module
  Address 0x3C.
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

const int W = 128;
const int H = 64;

Adafruit_SH1106G display(W, H, &Wire, -1);

void showMessage() {
  const char *text = "I hate U";
  const int textSize = 2;
  const int textW = 6 * textSize * 8;
  const int textH = 8 * textSize;

  display.clearDisplay();
  display.setTextColor(SH110X_WHITE);
  display.setTextSize(textSize);
  display.setTextWrap(false);
  display.setCursor((W - textW) / 2, (H - textH) / 2);
  display.print(text);
  display.display();
}

void setup() {
  Serial.begin(115200);
  delay(400);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Wire.begin();
  Wire.setClock(100000);

  bool ok = display.begin(0x3C, false);
  digitalWrite(LED_BUILTIN, ok ? LOW : HIGH);
  Serial.println(ok ? "OLED_OK" : "OLED_MISSING");
  if (ok) showMessage();
}

void loop() {
  if (digitalRead(LED_BUILTIN) == HIGH) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(180);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(180);
  }
}
