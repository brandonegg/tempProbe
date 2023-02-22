#include "temp_probe.h"

float temp_f = 32;
float temp_c = 0;

void collect_current_temp(TemperatureData* temp_data) {
    // TODO: Orlando hardware controls goes here.
    (*temp_data).record_reading(temp_c, temp_f);
    temp_f++;
    temp_c++;
}

/**
 * Temperature probe class functionality. Mostly getters and setters.
 */
TemperatureData::TemperatureData(OLEDManager* display, bool is_probe_connected) {
    oled = display;
    remote_display_on = false;
    probe_connected = is_probe_connected;
    current_c = 0.0f;
    current_f = 32.0f;
}

TemperatureData::TemperatureData(OLEDManager* display, bool is_probe_connected, float c, float f) {
    oled = display;
    remote_display_on = false;
    probe_connected = is_probe_connected;
    current_c = c;
    current_f = f;
}

void TemperatureData::record_reading(float c, float f) {
    current_c = c;
    current_f = f;

    oled->display_temperature(c, f);

    // Find new buffer location
    if (buff_pos >= TEMP_BUFFER_SIZE - 1) {
        buff_pos = 0;
    } else {
        buff_pos++;
    }

    if (buff_start >= TEMP_BUFFER_SIZE - 1) {
        buff_start = 0;
    } else {
        buff_start++;
    }

    // Insert
    bufferC[buff_pos] = current_c;
    bufferF[buff_pos] = current_f;
}

void TemperatureData::set_probe(bool connected) {
    probe_connected = connected;
}

String TemperatureData::temp_json_str() {
    String result = "{\"c\":" + String(current_c) + ",\"f\":" + String(current_f) + "}";
    return result;
}

float TemperatureData::get_c() {
    return current_c;
}

float TemperatureData::get_f() {
    return current_f;
}

bool TemperatureData::is_probe_connected() {
    return probe_connected;
}

String TemperatureData::get_history_c_str() {
    return get_buffer_str(&bufferC[0]);
}

String TemperatureData::get_history_f_str() {
    return get_buffer_str(&bufferF[0]);
}

bool TemperatureData::is_remote_display_enabled() {
    return remote_display_on;
}

void TemperatureData::set_remote_display_enabled(bool val) {
    remote_display_on = val;
}

/**
 * Used as a helper for get_history_*_str. Traverses buffer from oldest to newest
 * data point and creates JSON list representation.
 * @param float* buffer Pointer to start of buffer
 */
String TemperatureData::get_buffer_str(float* buffer) {
    signed int buffer_index = buff_start;
    String output = "[";

    for (int offset = 0; offset < TEMP_BUFFER_SIZE; offset++) {
        int i = buffer_index + offset;
        
        if (i >= TEMP_BUFFER_SIZE) {
            buffer_index = -offset;
            i = buffer_index + offset;
        }

        output += String(buffer[i]);
        if (offset < TEMP_BUFFER_SIZE-1) {
            output += ",";
        }
    }

    output += "]";
    return output;
}
