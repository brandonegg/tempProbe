
#include "web_server.h"
#include <ESPmDNS.h>

/*
 * TEMPERATURE SERVER FUNCTIONS
 */
WebServer* TemperatureServer::server;
PhoneAlertData* TemperatureServer::phone_alert;

TemperatureServer::TemperatureServer() {
    TemperatureServer::phone_alert = new PhoneAlertData();

    MDNS.begin("tempbox");
    TemperatureServer::server = new WebServer(80);
    // Routes
    TemperatureServer::server->on("/ping", HTTP_GET, handle_ping);
    TemperatureServer::server->on("/alert", HTTP_GET, handle_get_alert_data);
    TemperatureServer::server->onNotFound(handle_not_found);
    // Start server
    TemperatureServer::server->begin();

    Serial.println("Web Server has successfully started!");
}

void TemperatureServer::handle_client() {
    TemperatureServer::server->handleClient();
}

void TemperatureServer::handle_ping() {
    String response = {"{\"status\":\"active\", \"sensor_connected\":true}"};
    TemperatureServer::server->send(200, "application/json", response);
}

void TemperatureServer::handle_get_alert_data() {
    Serial.println("Collecting data");
    String* data = TemperatureServer::phone_alert->format_json();
    TemperatureServer::server->send(200, "application/json", (*data));
    delete data;
}

void TemperatureServer::handle_not_found() {
    TemperatureServer::server->send(404, "text/plain", "Not found");
}

/*
 * PHONE ALERT FUNCTIONS
 */
String* PhoneAlertData::format_json() {
    String* response = new String("{\"phone_number\":\"" + phone_number + "\",\"min_temp\":" + String(min_temp) + ",\"max_temp\":" + String(max_temp) + "}");
    return response;
}