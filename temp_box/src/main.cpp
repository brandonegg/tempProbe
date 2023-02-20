#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"
#include "temp_probe.h"

#define TEMPERATURE_POLL_FREQUENCY 1000000 // Once every 1 seconds (time in uS).
esp_timer_handle_t timer;

TemperatureServer* temp_server;
TemperatureData* temp_data;

void timed_calls(void* arg) {
  collect_current_temp(temp_data);
}

/**
 * Configuration needs to initialize web server and twilio manager.
 */
void setup() {
  Serial.begin(115200);
  connect_wifi();

  // Initialize objects
  temp_data = new TemperatureData(true);
  temp_server = new TemperatureServer(temp_data);

  // Timed function
  esp_timer_create_args_t timer_args = {
    .callback = &timed_calls,
    .arg = NULL,
    .name = "temp readings"
  };
  esp_timer_create(&timer_args, &timer);
  esp_timer_start_periodic(timer, TEMPERATURE_POLL_FREQUENCY);
  collect_current_temp(temp_data);
  collect_current_temp(temp_data);
}

/**
 * Listen for web server events and poll hardware
 */
void loop() {
  (*temp_server).listen();
}
