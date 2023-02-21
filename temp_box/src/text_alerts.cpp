#include "text_alerts.h"

TextManager::TextManager(TemperatureData* temp_data_in) {
    temp_data = temp_data_in;
    phone_data = new PhoneAlertData();
    twilio = new Twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);
    Serial.println("TextManager initialized - Twilio connected");
    bool prev_outside_range = false;
}

PhoneAlertData* TextManager::get_data() {
    return phone_data;
}

void TextManager::update_data(String phone_number, float min_temp, float max_temp, char unit) {
    phone_data->phone_number = phone_number;
    phone_data->min_temp = min_temp;
    phone_data->max_temp = max_temp;
    phone_data->unit = unit;
}

void TextManager::send_text_alert(String msg) {
    String response;
    bool success = twilio->send_message(phone_data->phone_number, TWILIO_FROM_NUMBER, msg, response);
    if (!success) {
        Serial.println("Failed sending text message!");
    }
}

void TextManager::check_temp() {
    float temp = temp_data->get_c();

    if (phone_data->unit == 'f') {
        temp = temp_data->get_f();
    }

    if (temp > phone_data->max_temp || temp < phone_data->min_temp) {
        if (!prev_outside_range) {
            Serial.println("sending text");
            String unit_upper = String(phone_data->unit);
            unit_upper.toUpperCase();

            send_text_alert("(Temperature = " + String(temp) + unit_upper + ") The temperature probe has fallen outside your threshold");
            prev_outside_range = true;
        }
    } else {
        prev_outside_range = false;
    }
}

/*
 * PHONE ALERT FUNCTIONS
 */
String* PhoneAlertData::format_json() {
    String* response = new String("{\"phone_number\":\"" + phone_number + "\",\"min_temp\":" + String(min_temp) + ",\"max_temp\":" + String(max_temp) + ",\"unit\":\"c\"}");
    return response;
}