
#include "web_server.h"
#include <ESPmDNS.h>

WebServer* TemperatureServer::server;

TemperatureServer::TemperatureServer() {
    MDNS.begin("tempbox");
    TemperatureServer::server = new WebServer(80);
    // Routes
    TemperatureServer::server->on("/hello", HTTP_GET, handle_hello);
    TemperatureServer::server->onNotFound(handle_not_found);
    // Start server
    TemperatureServer::server->begin();

    Serial.println("Web Server has successfully started!");
}

void TemperatureServer::handle_hello() {
    TemperatureServer::server->send(200, "text/plain", "hello world");
}

void TemperatureServer::handle_client() {
    TemperatureServer::server->handleClient();
}

void TemperatureServer::handle_not_found() {
    TemperatureServer::server->send(404, "text/plain", "Not found");
}