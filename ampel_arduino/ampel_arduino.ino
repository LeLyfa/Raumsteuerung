#include "Adafruit_WS2801.h"
#include "SPI.h" 

uint8_t dataPin  = 2;    
uint8_t clockPin = 3;    

Adafruit_WS2801 strip = Adafruit_WS2801(1, dataPin, clockPin);

void setup() {

  pinMode(12, INPUT);

  strip.begin();
  strip.show();
}


void loop() {
  if (digitalRead(12) == HIGH) {

    delay(1200);

    if (digitalRead(12) == LOW) {
      gruen();
      return;
    }

    delay(1000);

    if (digitalRead(12) == LOW) {
      gelb();
      return;
    }

    delay(1000);

    if (digitalRead(12) == LOW) {
      rot();
      return;
    }

  }
  delay(10);
}

// Bei den LED Treibern ist das Formst RBG

void gruen() {
  strip.setPixelColor(0, 0, 0, 255);
  strip.show();
}

void gelb() {
  strip.setPixelColor(0, 255, 0, 215);
  strip.show();
}

void rot() {
  flash();
  strip.setPixelColor(0, 255, 0, 0);
  strip.show();
}

void flash(){
  for (int i = 0; i != 6; i++) {
    strip.setPixelColor(0, 255, 0, 0);
    strip.show();
    delay(250);
    strip.setPixelColor(0, 0, 0, 0);
    strip.show();
    delay(250);
  }
}
