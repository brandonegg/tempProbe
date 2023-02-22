#ifndef OLED_DISPLAY
#define OLED_DISPLAY
#include <U8g2lib.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

class OLEDManager {
    public:
        /**
         * Initialize display
         */
        OLEDManager();
        /**
         * Output temperatures to the display
         */
        void display_temperature(float c, float f);
        /**
         * Render text to LCD
         * @param int x x coordinate of text
         * @param int y y coordinate of text
         */
        void render_text(int x, int y, String msg);
        /**
         * Clears display.
         */
        void clear(void);
        /**
         * Sends buffer to display
         */
        void send();

    private:
        U8G2_SSD1306_128X64_NONAME_F_SW_I2C* u8g2;
};

#endif