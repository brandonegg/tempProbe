#ifndef TEXT_MANAGER
#define TEXT_MANAGER
#include <Arduino.h>
#include "secrets.h"
#include "twilio.hpp"
#include "temp_probe.h"

#define TWILIO_FROM_NUMBER "+18885719233"

/**
 * Object for storing twilio phone data, trigger temps & phone.
 */
class PhoneAlertData {
    public:
        String phone_number = "";
        int min_temp = 0;
        int max_temp = 100;
        char unit = 'c';
        String* format_json();
};

class TextManager {
    public:
        /**
         * As TemperatureData object is used to determine current temperature and if
         * it falls outside threshold.
         */
        TextManager(TemperatureData* temp_data_in);
        /**
         * Pass new phone number data to class
         */
        void update_data(String phone_number, float min_temp, float max_temp, char unit);
        /**
         * Check current temperature data. Should be called in main routine loop.
         */
        void check_temp();
        /**
         * Getter for phone alert data reference
         */
        PhoneAlertData* get_data();

    private:
        PhoneAlertData* phone_data;
        TemperatureData* temp_data;
        Twilio* twilio;
        void send_text_alert(String msg);
        /**
         * Whether the previously initialized data was outside the set temp range.
         * Used to determine if new text needs to be sent.
         */
        bool prev_outside_range = false;
};

#endif