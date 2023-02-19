#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"

TemperatureServer *temp_server;

void setup() {
  Serial.begin(115200);
  connect_wifi();
  temp_server = new TemperatureServer();
}

void loop() {
  (*temp_server).listen();
}
