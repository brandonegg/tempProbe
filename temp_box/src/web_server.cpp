
#include "web_server.h"
#include <ESPmDNS.h>
#include <ArduinoJson.h>

/*
 * TEMPERATURE SERVER FUNCTIONS
 */
WebServer* TemperatureServer::server;
PhoneAlertData* TemperatureServer::phone_alert;
TemperatureData* TemperatureServer::temp_data;
TextManager* TemperatureServer::text_manager;

/**
 * TemperatureServer class initializes webserver on port 80 (with mdns tempbox.local). Adds
 * all route listeners which typically are written as handle_{request_type}_{endpoint_endpoint_endpoint...}
 * 
 * @param TemperatureData temp_data Reference to the temp data object for pull current temps from.
 */
TemperatureServer::TemperatureServer(TemperatureData* temp_data, TextManager* text_manager) {
    TemperatureServer::temp_data = temp_data;
    TemperatureServer::phone_alert = new PhoneAlertData();
    TemperatureServer::text_manager = text_manager;

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
    String* data = text_manager->get_data()->format_json();
    TemperatureServer::server->send(200, "application/json", (*data));
    delete data;
}

void TemperatureServer::handle_get_history() {
    String response = "{\"c\":";
    response += TemperatureServer::temp_data->get_history_c_str();
    response += ",\"f\":";
    response += TemperatureServer::temp_data->get_history_f_str();
    response += ",\"sensor_connected\":" + String(TemperatureServer::temp_data->is_probe_connected());
    response += "}";
    TemperatureServer::server->send(200, "application/json", response);
}

void TemperatureServer::handle_post_alert() {
    DynamicJsonDocument doc(512);
    deserializeJson(doc, TemperatureServer::server->arg("plain"));

    String phone_number = doc["phone_number"].as<String>();
    float min_temp = doc["min_temp"].as<float>();
    float max_temp = doc["max_temp"].as<float>();
    char unit = doc["unit"].as<String>().charAt(0);

    text_manager->update_data(phone_number, min_temp, max_temp, unit);

    TemperatureServer::server->send(200, "application/json", "{\"success\":true}");
}

void TemperatureServer::handle_not_found() {
    TemperatureServer::server->send(404, "text/plain", "Not found");
}
