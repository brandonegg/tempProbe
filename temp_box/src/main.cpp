#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"
#include "temp_probe.h"

TemperatureServer* temp_server;
TemperatureData* temp_data;

/**
 * Configuration needs to initialize web server and twilio manager.
 */
void setup() {
  Serial.begin(115200);
  connect_wifi();

  // Initialize objects
  temp_data = new TemperatureData(true);
  temp_server = new TemperatureServer(temp_data);
}

/**
 * Listen for web server events and poll hardware
 */
void loop() {
  (*temp_server).listen();
}
