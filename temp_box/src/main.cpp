#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"
#include "temp_probe.h"
#include "oled.h"

#define DISPLAY_BUTTON_PIN 48
#define TEMPERATURE_POLL_FREQUENCY 1000000 // Once every 1 seconds (time in uS).
esp_timer_handle_t timer;

TemperatureServer* temp_server;
TemperatureData* temp_data;
TextManager* text_manager;
OLEDManager* oled;

void timed_calls(void* arg) {
  bool result = collect_current_temp(temp_data);
  if (!result) {
    // Not connected
    temp_data->set_probe(false);
  } else {
    temp_data->set_probe(true);
  }
}

/**
 * Configuration needs to initialize web server and twilio manager.
 */
void setup() {
  Serial.begin(115200);
  oled = new OLEDManager();
  oled->set_display(true);
  oled->render_text(0,28, "Connecting to WiFi:", u8g2_font_6x13O_tr);
  oled->render_text(0,42, WIFI_SSID, u8g2_font_6x13B_tf);
  oled->send();

  connect_wifi();

  // Initialize objects
  temp_data = new TemperatureData(oled, true);
  text_manager = new TextManager(temp_data);
  temp_server = new TemperatureServer(temp_data, text_manager);

  // Init hardware
  init_temperature_probe();

  // Timed function
  esp_timer_create_args_t timer_args = {
    .callback = &timed_calls,
    .arg = NULL,
    .name = "temp readings"
  };
  esp_timer_create(&timer_args, &timer);
  esp_timer_start_periodic(timer, TEMPERATURE_POLL_FREQUENCY);
  collect_current_temp(temp_data);
  oled->set_display(false);

  // Setup push button
  pinMode(DISPLAY_BUTTON_PIN, INPUT);
}

/**
 * Listen for web server events and poll hardware
 */
void loop() {
  int btn_state = digitalRead(DISPLAY_BUTTON_PIN);
  if (btn_state == HIGH || temp_data->is_remote_display_enabled()) {
    oled->set_display(true);
  } else {
    oled->set_display(false);
  }

  temp_server->listen();
  text_manager->check_temp();
}
