#ifndef TEMP_HARDWARE
#define TEMP_HARDWARE
#include <Arduino.h>

#define TEMP_BUFFER_SIZE 300

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
         * Sets whether the temp probe is connected
         * @param bool connected true/false for connected/not connected
         */
        void set_probe(bool connected);

        /**
         * Formats to the style {"c": ..., "f": ...}
         * @returns Temperature json string formatted for web router.
         */
        String temp_json_str();

        /**
         * @returns Most recent celsius temperature reading.
         */
        float get_c();
        /**
         * @returns Most recent fahrenheit temperature reading.
         */
        float get_f();
        /**
         * Gets whether the prob is connected.
         */
        bool is_probe_connected();
        /**
         * Returns JSON list string for temp buffer.
         */
        String get_history_c_str();
        /**
         * Returns JSON list string for temp buffer.
         */
        String get_history_f_str();


    private:
        float bufferC[TEMP_BUFFER_SIZE] = { 0.0f };
        float bufferF[TEMP_BUFFER_SIZE] = { 0.0f };
        int buff_pos = 0;
        int buff_start = 1;
        bool probe_connected;
        float current_c;
        float current_f;

        String get_buffer_str(float* buffer);
};

/**
 * Interfaces with hardware to collect current temperature data.
 */
void collect_current_temp(TemperatureData* temp_data);

#endif
