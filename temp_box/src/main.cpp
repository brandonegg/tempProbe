#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"

TemperatureServer *temp_server;

/**
 * Configuration needs to initialize web server and twilio manager.
 */
void setup() {
  Serial.begin(115200);
  connect_wifi();
  temp_server = new TemperatureServer();
}

/**
 * Listen for web server events and poll hardware
 */
void loop() {
  (*temp_server).listen();
}
