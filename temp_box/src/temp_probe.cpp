#include "temp_probe.h"

/**
 * Temperature probe class functionality. Mostly getters and setters.
 */
TemperatureData::TemperatureData() {
    current_c = 0.0f;
    current_f = 32.0f;
}

TemperatureData::TemperatureData(float c, float f) {
    current_c = c;
    current_f = f;
}

void TemperatureData::record_reading(float c, float f) {
    current_c = c;
    current_f = f;
}

String TemperatureData::temp_json_str() {
    String result = "{\"c\":" + String(current_c) + ",\"f\":" + String(current_f) + "}";
    return result;
}

int TemperatureData::get_c() {
    return current_c;
}

int TemperatureData::get_f() {
    return current_f;
}
