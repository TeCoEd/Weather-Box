# Import library and create instance of REST client.

from Adafruit_IO import RequestError, Client, Feed
from PIL import Image, ImageDraw, ImageFont
import random
from time import sleep

import logging
import ST7735
from bme280 import BME280

# PREPARE THE LIGHT SENSOR ######################
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

# PREPARE THE PRESSURE SENSOR ###############################
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Pimoroni code to display message on screen ##############
# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()

#sleep(60)

try:
    #################################################################    
    # Sign in details ##############################################
    ADAFRUIT_IO_USERNAME = 'Your User Name'
    ADAFRUIT_IO_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Feeds to send the data too
    gas =aio.feeds("gas")
    humidity = aio.feeds("humidity")
    light = aio.feeds("light")
    pressure = aio.feeds("pressure")
    temperature = aio.feeds("temperature")
    rain = aio.feeds("rain") 

    while True:
        # Width and height to calculate text position.
        WIDTH = disp.width
        HEIGHT = disp.height

        # New canvas to draw on.
        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Text settings.
        font_size = 25
        font = ImageFont.truetype("fonts/Asap/Asap-Bold.ttf", font_size)
        text_colour = (0, 255, 0)
        back_colour = (0, 0, 0)

        message = "DA WEATHER!"
        size_x, size_y = draw.textsize(message, font)

        # Calculate text position
        x = (WIDTH - size_x) / 2
        y = (HEIGHT / 2) - (size_y / 2)

        # Draw background rectangle and write text.
        draw.rectangle((0, 0, 160, 80), back_colour)
        draw.text((x, y), message, font=font, fill=text_colour)
        disp.display(img)

         ### Upload the data###

        ###############################################################
        ######### readings ############################################
        ###############################################################
    
        # Collect data from Enviro+
        # ADD GAS
        humidity_reading = bme280.get_humidity()    
        lux = ltr559.get_lux() # light
        pressure_reading = bme280.get_pressure() # pressure
        temperature_read = bme280.get_temperature()
            
        # ADD GAS
        aio.send_data(humidity.key, humidity_reading)
        aio.send_data(light.key, (lux/10))
        aio.send_data(pressure.key, pressure_reading)
        aio.send_data(temperature.key, temperature_read-11)

        # Chance of rain calculation
        if pressure_reading < 998: #may need to change this
            chance_of_rain = 90
        else:
            chance_of_rain = 1050 - pressure_reading #need to calabrate
            
        aio.send_data(rain.key, chance_of_rain)

        print ("data sent")
        sleep(900) # 15 x 60

except:
    print ("NO INTERNET CONNECTION")
    # Width and height to calculate text position.
    WIDTH = disp.width
    HEIGHT = disp.height

    # New canvas to draw on.
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Text settings.
    font_size = 25
    font = ImageFont.truetype("fonts/Asap/Asap-Bold.ttf", font_size)
    text_colour = (255, 0, 0)
    back_colour = (0, 0, 0)

    message = "NO INTERNET!"
    size_x, size_y = draw.textsize(message, font)

    # Calculate text position
    x = (WIDTH - size_x) / 2
    y = (HEIGHT / 2) - (size_y / 2)

    # Draw background rectangle and write text.
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), message, font=font, fill=text_colour)
    disp.display(img)
        
    # works the same as send now
    #aio.append(temperature.key, 42)'''



