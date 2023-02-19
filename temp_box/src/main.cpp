#include "wifi_util.h"
#include "secrets.h"
#include <WiFi.h> //Wifi library
#include "web_server.h"

TemperatureServer *temp_server;

const char* host = "temperature.box"; //webserver
String url = "/eduroam/data.php"; //URL to target PHP file

void http_request() {
  WiFiClient client;
  delay(1000);
  client.stop();
  String data = "ssid=" + String(WIFI_SSID) + "&identity=" + String(EAP_IDENTITY) + "&anonymous_identity=" + String(EAP_IDENTITY);
  if (client.connect(host, 80)) {
    Serial.println(F("Connected to webserver!"));
    client.println("POST " + url + " HTTP/1.0");
    client.println("Host: " + (String)host);
    client.println(F("User-Agent: ESP32"));
    client.println(F("Connection: close"));
    client.println(F("Content-Type: application/x-www-form-urlencoded;"));
    client.print(F("Content-Length: "));
    client.println(data.length());
    client.println();
    client.println(data);
    Serial.println(F("Data received by server, THANKS for trying this eduroam connection example!"));
    while (client.connected()) {
      String line = client.readStringUntil('\n'); //HTTP HEADER
      if (line == "\r") {
        break;
      }
    }
    String line = client.readStringUntil('\n'); //HTTP PAYLOAD
  } else {
    Serial.println(F("Connection wasn't sucessful, try again later"));
  }
}

void setup() {
  Serial.begin(115200);
  connect_wifi();
  temp_server = new TemperatureServer();
  //http_request(); //I will receive information about successful connection and identity realm (i can write it into Github project page as u have tested it)
}

void loop() {
  (*temp_server).listen();
}
