#include "temp_probe.h"

/**
 * Temperature probe class functionality. Mostly getters and setters.
 */
TemperatureData::TemperatureData(bool is_probe_connected) {
    probe_connected = is_probe_connected;
    current_c = 0.0f;
    current_f = 32.0f;
}

TemperatureData::TemperatureData(bool is_probe_connected, float c, float f) {
    probe_connected = is_probe_connected;
    current_c = c;
    current_f = f;
}

void TemperatureData::record_reading(float c, float f) {
    current_c = c;
    current_f = f;
}

void TemperatureData::set_probe(bool connected) {
    probe_connected = connected;
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

bool TemperatureData::is_probe_connected() {
    return probe_connected;
}
