#ifndef TEMP_HARDWARE
#define TEMP_HARDWARE
#include <Arduino.h>

class TemperatureData {
    public:
        String get_history_string(char unit);

        TemperatureData();
        /**
         * Overload function with option to construct with starting temperatures.
         */
        TemperatureData(int c, int f);
        
        /**
         * Use to add a temperature reading to the log.
         * @param int c Reading in celsius
         * @param int f Reading in fahrenheit
         */
        void record_reading(int c, int f);

        /**
         * @returns Most recent celsius temperature reading.
         */
        int get_c();
        /**
         * @returns Most recent fahrenheit temperature reading.
         */
        int get_f();

    private:
        int current_c = 0;
        int current_f = 0;
};

#endif