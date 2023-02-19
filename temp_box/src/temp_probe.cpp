#include "temp_probe.h"

/**
 * Temperature probe class functionality. Mostly getters and setters.
 */

TemperatureData::TemperatureData(int c, int f) {
    current_c = c;
    current_f = f;
}

void TemperatureData::record_reading(int c, int f) {
    current_c = c;
    current_f = f;
}

int TemperatureData::get_c() {
    return current_c;
}

int TemperatureData::get_f() {
    return current_f;
}
