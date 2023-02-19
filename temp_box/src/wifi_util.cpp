#include "wifi_util.h"
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks
#include <WiFi.h> //Wifi library
#include "secrets.h"

byte mac[6];

void setup_eduroam() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WPA2_AUTH_PEAP, EAP_ANONYMOUS_IDENTITY, EAP_IDENTITY, EAP_PASSWORD); //WITHOUT CERTIFICATE - WORKING WITH EXCEPTION ON RADIUS SERVER
}

void setup_other() {
  WiFi.begin(WIFI_SSID, EAP_PASSWORD);
}

void connect_wifi() {
    WiFi.disconnect(true);  //disconnect from WiFi to set new WiFi connection
    if (strcmp(WIFI_SSID, "eduroam") == 0) {
        Serial.println("Configuring WiFi for eduroam authentication");
        setup_eduroam();
    } else {
        setup_other();
    }

    Serial.print(F("Connecting to network: "));
    Serial.println(WIFI_SSID);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(F("."));
    }

    Serial.println("");
    Serial.println(F("WiFi is connected!"));
    Serial.println(F("IP address set: "));
    Serial.println(WiFi.localIP()); //print LAN IP
    WiFi.macAddress(mac);
    Serial.print("MAC address: ");
    Serial.print(mac[0], HEX);
    Serial.print(":");
    Serial.print(mac[1], HEX);
    Serial.print(":");
    Serial.print(mac[2], HEX);
    Serial.print(":");
    Serial.print(mac[3], HEX);
    Serial.print(":");
    Serial.print(mac[4], HEX);
    Serial.print(":");
    Serial.println(mac[5], HEX);
}