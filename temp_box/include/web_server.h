#ifndef TEMPERATURE_SERVER
#define TEMPERATURE_SERVER
#include <WebServer.h>
#include "temp_probe.h"
#include "text_alerts.h"

/**
 * WebServer object controller. Configures and handles incomming web traffic.
 * One instance of this class should be made during runtime, object members are static.
 */
class TemperatureServer {

    public:
        TemperatureServer(TemperatureData* temp_data, TextManager* text_manager);
        static void listen();

        int temp_buffer[300] = { };

    private:
        // Static members initialized by class constructor.
        static WebServer* server;
        static PhoneAlertData* phone_alert;
        static TemperatureData* temp_data;
        static TextManager* text_manager;
        char reference = 'c'; // c or f - use LOWER case.
        
        // Route handlers - format = handle_{method}_{endpoint}
        static void handle_get_alert();
        static void handle_post_alert();
        static void handle_get_ping();
        static void handle_get_history();
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