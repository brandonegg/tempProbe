#ifndef TEMP_HARDWARE
#define TEMP_HARDWARE
#include <Arduino.h>

class TemperatureData {
    public:
        String get_history_string(char unit);

        TemperatureData(bool is_prob_connected);
        /**
         * Overload function with option to construct with starting temperatures.
         */
        TemperatureData(bool is_prob_connected, float c, float f);
        
        /**
         * Use to add a temperature reading to the log.
         * @param int c Reading in celsius
         * @param int f Reading in fahrenheit
         */
        void record_reading(float c, float f);

        /**
         * Formats to the style {"c": ..., "f": ...}
         * @returns Temperature json string formatted for web router.
         */
        String temp_json_str();

        /**
         * @returns Most recent celsius temperature reading.
         */
        int get_c();
        /**
         * @returns Most recent fahrenheit temperature reading.
         */
        int get_f();
        /**
         * Gets whether the prob is connected.
         */
        bool is_probe_connected();

    private:
        bool probe_connected;
        float current_c;
        float current_f;
};

#endif