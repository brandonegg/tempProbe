#ifndef TEMPERATURE_SERVER
#define TEMPERATURE_SERVER
#include <WebServer.h>

class TemperatureServer {

    public:
        TemperatureServer();
        static void handle_client();

    private:
        static WebServer *server;
        static void handle_hello();
        static void handle_not_found();
};

#endif