
#include "web_server.h"
#include <ESPmDNS.h>
#include <ArduinoJson.h>

/*
 * TEMPERATURE SERVER FUNCTIONS
 */
WebServer* TemperatureServer::server;
PhoneAlertData* TemperatureServer::phone_alert;
TemperatureData* TemperatureServer::temp_data;

/**
 * TemperatureServer class initializes webserver on port 80 (with mdns tempbox.local). Adds
 * all route listeners which typically are written as handle_{request_type}_{endpoint_endpoint_endpoint...}
 * 
 * @param TemperatureData temp_data Reference to the temp data object for pull current temps from.
 */
TemperatureServer::TemperatureServer(TemperatureData* temp_data) {
    TemperatureServer::temp_data = temp_data;
    TemperatureServer::phone_alert = new PhoneAlertData();

    MDNS.begin("tempbox");
    TemperatureServer::server = new WebServer(80);
    // Routes
    TemperatureServer::server->on("/ping", HTTP_GET, handle_get_ping);
    TemperatureServer::server->on("/alert", HTTP_GET, handle_get_alert);
    TemperatureServer::server->on("/alert", HTTP_POST, handle_post_alert);
    TemperatureServer::server->on("/history", HTTP_GET, handle_get_history);
    TemperatureServer::server->onNotFound(handle_not_found);
    // Start server
    TemperatureServer::server->begin();

    Serial.println("Web Server has successfully started!");
}

/**
 * Extension to WebServer's handleClient utility. Should be placed in loop() to trigger
 * the route listeners on incomming request.
 */
void TemperatureServer::listen() {
    TemperatureServer::server->handleClient();
}

/**
 * Handles the /ping route for the web server. Returns status information for the device
 * such as sensor_connected (whether temp probe is connected), and current temperature data.
 */
void TemperatureServer::handle_get_ping() {
    String response = "{\"status\":\"active\"";
    response += ",\"sensor_connected\":" + String(TemperatureServer::temp_data->is_probe_connected());
    response += ",\"temperature\":" + TemperatureServer::temp_data->temp_json_str();
    response += "}";
    TemperatureServer::server->send(200, "application/json", response);
}

void TemperatureServer::handle_get_alert() {
    String* data = TemperatureServer::phone_alert->format_json();
    TemperatureServer::server->send(200, "application/json", (*data));
    delete data;
}

void TemperatureServer::handle_get_history() {
    String response = "{\"c\":";
    response += TemperatureServer::temp_data->get_history_c_str();
    response += ",\"f\":";
    response += TemperatureServer::temp_data->get_history_f_str();
    response += "}";
    TemperatureServer::server->send(200, "application/json", response);
}

void TemperatureServer::handle_post_alert() {
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, TemperatureServer::server->arg("plain"));

    TemperatureServer::phone_alert->phone_number = doc["phone_number"].as<String>();
    TemperatureServer::phone_alert->min_temp = doc["min_temp"].as<int>();
    TemperatureServer::phone_alert->max_temp = doc["max_temp"].as<int>();
    TemperatureServer::phone_alert->unit = doc["unit"].as<String>().charAt(0);

    TemperatureServer::server->send(200, "application/json", "{\"success\":true}");
}

void TemperatureServer::handle_not_found() {
    TemperatureServer::server->send(404, "text/plain", "Not found");
}

/*
 * PHONE ALERT FUNCTIONS
 */
String* PhoneAlertData::format_json() {
    String* response = new String("{\"phone_number\":\"" + phone_number + "\",\"min_temp\":" + String(min_temp) + ",\"max_temp\":" + String(max_temp) + ",\"unit\":\"c\"}");
    return response;
}