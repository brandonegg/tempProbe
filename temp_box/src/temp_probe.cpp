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
    return get_buffer_str(bufferC);
}

String TemperatureData::get_history_f_str() {
    return get_buffer_str(bufferF);
}

/**
 * Used as a helper for get_history_*_str. Traverses buffer from oldest to newest
 * data point and creates JSON list representation.
 * @param float* buffer Pointer to start of buffer
 */
String TemperatureData::get_buffer_str(float* buffer) {
    int buffer_index = buff_start;
    String output = "[";

    for (int offset = 0; offset < TEMP_BUFFER_SIZE; offset++) {
        int i = buffer_index + offset;
        
        if (i >= TEMP_BUFFER_SIZE) {
            i = offset;
        }

        output += String(buffer[i]);
        if (offset < TEMP_BUFFER_SIZE-1) {
            output += ",";
        }
    }

    output += "]";
    return output;
}
