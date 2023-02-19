#ifndef TEMPERATURE_SERVER
#define TEMPERATURE_SERVER
#include <WebServer.h>
#include "temp_probe.h"

/**
 * Object for storing twilio phone data, trigger temps & phone.
 */
class PhoneAlertData {
    public:
        String phone_number = "";
        int min_temp = 0;
        int max_temp = 100;
        char unit = 'c';
        String* format_json();
};

/**
 * WebServer object controller. Configures and handles incomming web traffic.
 * One instance of this class should be made during runtime, object members are static.
 */
class TemperatureServer {

    public:
        TemperatureServer(TemperatureData* temp_data);
        static void listen();

        int temp_buffer[300] = { };

    private:
        // Static members initialized by class constructor.
        static WebServer* server;
        static PhoneAlertData* phone_alert;
        static TemperatureData *temp_data;
        char reference = 'c'; // c or f - use LOWER case.
        
        // Route handlers - format = handle_{method}_{endpoint}
        static void handle_get_alert();
        static void handle_post_alert();
        static void handle_ping();
        // 404 default
        static void handle_not_found();
};

/*
class FlashManager {
    public:
        FlashManager();
        char load_reference_mode();
        store_reference_mode(char val);
        store_phone_data(*PhoneAlert phone_data);
}
*/

#endif