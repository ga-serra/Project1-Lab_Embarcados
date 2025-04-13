from machine import Pin, SoftI2C
import ssd1306

i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))

display = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

def send_message_clear(msg, x, y):
    display.fill(0)
    display.text(msg, x, y)
    display.show()
