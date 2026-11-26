/*
  Shows I + a drawn heart + lsy on the SH1106.
  Arduino UNO R4 WiFi
  OLED -> SDA A4, SCL A5, GND, VCC as printed on the module
  Address 0x3C. The built-in font has no heart glyph, so the heart is drawn.
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

const int W = 128;
const int H = 64;

Adafruit_SH1106G display(W, H, &Wire, -1);

void drawHeart(int x, int y) {
  display.fillCircle(x + 6, y + 6, 6, SH110X_WHITE);
  display.fillCircle(x + 16, y + 6, 6, SH110X_WHITE);
  display.fillTriangle(x + 1, y + 8, x + 21, y + 8, x + 11, y + 20, SH110X_WHITE);
}

void showMessage() {
  const int textSize = 3;
  const int cell = 6 * textSize;
  const int textH = 8 * textSize;
  const int heartW = 22;
  const int gap = 3;
  const int total = cell + gap + heartW + gap + (cell * 3);
  const int x0 = (W - total) / 2;
  const int textY = (H - textH) / 2;

  display.clearDisplay();
  display.setTextColor(SH110X_WHITE);
  display.setTextSize(textSize);
  display.setTextWrap(false);

  display.setCursor(x0, textY);
  display.print("I");

  drawHeart(x0 + cell + gap, textY + 2);

  display.setCursor(x0 + cell + gap + heartW + gap, textY);
  display.print("lsy");

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
