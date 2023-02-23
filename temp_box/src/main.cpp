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

bool flag_disconnect_error = false;

void timed_calls(void* arg) {
  bool result = collect_current_temp(temp_data);
  Serial.println("Is probe connected? " + String(temp_data->is_probe_connected()));
  if (!result) {
    bool was_probe_connected_before = temp_data->is_probe_connected();
    // Not connected
    temp_data->set_probe(false);

    if (was_probe_connected_before) {
      // If this is the first time seeing it is not connected, render the display.
      flag_disconnect_error = true;
    }
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

  IPAddress ip = connect_wifi();
  oled->clear();
  oled->render_text(0,48, ip.toString(), u8g2_font_6x13B_tf);

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
  delay(3000);
  oled->set_display(false);

  // Setup push button
  pinMode(DISPLAY_BUTTON_PIN, INPUT);
}

/**
 * Listen for web server events and poll hardware
 */
void loop() {
  int btn_state = digitalRead(DISPLAY_BUTTON_PIN);
  if (btn_state == HIGH || temp_data->is_remote_display_enabled() || !temp_data->is_probe_connected()) {
    Serial.println("display on");
    oled->set_display(true);
    if (flag_disconnect_error) {
      oled->clear();
      oled->render_text(0, 15, "Error: Could not read", u8g2_font_6x13B_tf);
      oled->render_text(0, 30, "temperature data", u8g2_font_6x13B_tf);
      oled->send();
      Serial.println("Dispalying the text");
      flag_disconnect_error = false;
    }
  } else {
    oled->set_display(false);
  }

  temp_server->listen();
  text_manager->check_temp();
}
