#include "text_alerts.h"

TextManager::TextManager(TemperatureData* temp_data_in) {
    temp_data = temp_data_in;
    data = new PhoneAlertData();
    twilio = new Twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);
    bool prev_outside_range = false;
}

void TextManager::update_data(String phone_number, float min_temp, float max_temp, char unit) {
    data->phone_number = phone_number;
    data->min_temp = min_temp;
    data->max_temp = max_temp;
    data->unit = unit;
}

void TextManager::send_text_alert(String msg) {
    String response;
    bool success = twilio->send_message(data->phone_number, TWILIO_FROM_NUMBER, msg, response);
    if (!success) {
        Serial.println("Failed sending text message!");
    }
}

void TextManager::check_temp() {
    float temp = temp_data->get_c();

    if (data->unit == 'c') {
        temp = temp_data->get_f();
    }

    if (temp > data->max_temp || temp < data->min_temp) {
        if (!prev_outside_range) {
            send_text_alert("(Temperature = " + String(temp) + ") The temperature probe has fallen outside your threshold");
            prev_outside_range = true;
        }
    } else {
        prev_outside_range = false;
    }
}