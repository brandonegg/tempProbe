#ifndef TEMPERATURE_SERVER
#define TEMPERATURE_SERVER
#include <WebServer.h>

class PhoneAlertData {
    public:
        String phone_number = "";
        int min_temp = 0;
        int max_temp = 100;
        String* format_json();
};

class TemperatureServer {

    public:
        TemperatureServer();
        static void handle_client();

        int temp_buffer[300] = { };

    private:
        static WebServer *server;
        static PhoneAlertData* phone_alert;
        char reference = 'c'; // C or F
        
        // Temperature Alert CRUD
        static void handle_get_alert_data();

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