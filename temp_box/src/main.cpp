#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"
#include "temp_probe.h"
#include "oled.h"

#define TEMPERATURE_POLL_FREQUENCY 1000000 // Once every 1 seconds (time in uS).
esp_timer_handle_t timer;

TemperatureServer* temp_server;
TemperatureData* temp_data;
TextManager* text_manager;
OLEDManager* oled;

void timed_calls(void* arg) {
  collect_current_temp(temp_data);
}

/**
 * Configuration needs to initialize web server and twilio manager.
 */
void setup() {
  Serial.begin(115200);
  oled = new OLEDManager();
  oled->render_text(0,30, "Connected to WiFi:");
  oled->render_text(0,40, WIFI_SSID);
  oled->send();

  connect_wifi();

  // Initialize objects
  temp_data = new TemperatureData(oled, true);
  text_manager = new TextManager(temp_data);
  temp_server = new TemperatureServer(temp_data, text_manager);

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
  oled->clear();
}

/**
 * Listen for web server events and poll hardware
 */
void loop() {
  temp_server->listen();
  text_manager->check_temp();
}

void VextON(void)
{
  pinMode(Vext,OUTPUT);
  digitalWrite(Vext, LOW);
}

void VextOFF(void) //Vext default OFF
{
  pinMode(Vext,OUTPUT);
  digitalWrite(Vext, HIGH);
}
