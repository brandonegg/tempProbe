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
         * Render text to LCD - Requires sent() command afterwards for string to
         * display
         * @param int x x coordinate of text
         * @param int y y coordinate of text
         */
        void render_text(int x, int y, String msg, const uint8_t* font);
        /**
         * Clears display.
         */
        void clear(void);
        /**
         * Sends buffer to display
         */
        void send();
        /**
         * Sets the display to on (if true) or off.
         */
        void set_display(bool on);
        /**
         * Returns true is display is on
         */
        bool is_display_on();

    private:
        bool display_on = false;

    private:
        U8G2_SSD1306_128X64_NONAME_F_SW_I2C* u8g2;
};

#endif