# a programme to display today's weather and tomorrow
# on the inky_display using the OpenWeather API

#!/usr/bin/python3

import os
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
import datetime
from datetime import date, timedelta
import textwrap
import requests
import json

project_location = '/home/dietpi/inkyphat_weather'
# set the colour of the phat
inky_display = InkyPHAT('yellow')
#invert the screen (power cable on top) if needed.
inky_display.h_flip = True
inky_display.v_flip = True

# set lat/long for location and units
lat = 55.7132
lon = -3.2041

# set OpenWeather API Key
APIKEY = '<api_key>'

##request data from OpenWeather 'One Call' API
url = (
    f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&"
    f"units=metric&appid={APIKEY}")
r = requests.get(url)
weather_data = json.loads(r.text)

##test script to check JSON request result
with open('weather_text.json', 'w') as f:
  json.dump(weather_data, f, indent=2)
  f.close()
print(weather_data)
# # Get data needed from downloaded data
temp = weather_data['main']['temp']
current_conditions = weather_data['weather'][0]['description']
icon_code = weather_data['weather'][0]['icon']
icon_desc = weather_data['weather'][0]['main']
relative_humidity = weather_data['main']['humidity']
dew_point = 0 #weather_data['main']['dew_point']
wind_speed = weather_data['wind']['speed']
wind_gust = weather_data['wind']['gust']
wind_bearing = weather_data['wind']['deg']
pressure = weather_data['main']['pressure']
high_temp = weather_data['main']['temp_max']
low_temp = weather_data['main']['temp_min']

# format today's variables to current temp and high and low temps for the day
current_temp = round(temp)
current_temp = str(current_temp) + '°'
current_temp_F = round((1.8 * temp) + 32)
current_temp_F = str(current_temp_F) + 'F'
high_temp = round(high_temp)
low_temp = round(low_temp)
temps_today = 'Low ' + str(low_temp) + ' High ' + str(high_temp)
dew_point = round(dew_point)
dew_point = ' dew ' + str(dew_point) + 'C'
pressure = round(pressure)
pressure = str(pressure) + ' hPa'

# convert the wind bearing to a compass direction using a tuple of
# 16 compass points.
# We need to do windBearing  modulo 360 first
# to allow for 0 degree bearing.
wind_dir = ('N','NE','E','SE','S','SW','W','NW','N')
wind_bearing = wind_bearing % 360
wind_index = round(wind_bearing/ 45)
compass_dir = wind_dir[wind_index]

# format windspeeds, convert metres/second to mph and round
wind_speed = (wind_speed * 2.237)
wind_speed = round(wind_speed)
wind_gust = (wind_gust * 2.237)
wind_gust = round(wind_gust)

# #determine Beaufort scale number and wind description from wind speed
if wind_speed < 1:
    wind_desc = 'Calm'
    Beaufort =- 0
elif (wind_speed >= 1 and wind_speed <= 3):
    wind_desc = 'Light Air'
    Beaufort = 1
elif wind_speed <= 7:
    wind_desc = 'Light Breeze'
    Beaufort = 2
elif wind_speed <= 12:
    wind_desc = 'Gentle Breeze'
    Beaufort = 3
elif wind_speed <= 18:
    wind_desc = 'Moderate Breeze'
    Beaufort = 4
elif wind_speed <= 24:
    wind_desc = 'Fresh Breeze'
    Beaufort = 5
elif wind_speed <= 31:
    wind_desc = 'Strong Breeze'
    Beaufort = 6
elif wind_speed <= 38:
    wind_desc = 'Near Gale'
    Beaufort = 7
elif wind_speed <= 46:
    wind_desc = 'Gale'
    Beaufort = 8
elif wind_speed <= 54:
    wind_desc = 'Strong Gale'
    Beaufort = 9
elif wind_speed <= 63:
    wind_desc = 'Storm'
    Beaufort = 10
elif wind_speed <= 72:
    wind_desc = 'Violent Storm'
    Beaufort = 11
else:
    wind_desc = 'Hurricane'
    Beaufort = 12

# # prepare info for  line about the wind speed and Beaufort scale
gust = ' gust ' + str(wind_gust)
wind = str(wind_speed) + ' ' + compass_dir + gust

# # prepare info for line 3 which is Beaufort scale and dewpoint and
line3 = 'Bft.' + str(Beaufort) + ' ' + dew_point

# This imports three classes from PIL that we'll need, creates a new blank
# image 'img', that is the width and height of the Inky pHAT display, and then
# creates a drawing canvas, 'draw', to which we can draw text and graphics
img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# import our fonts
temp_font = ImageFont.truetype(f'{project_location}/fonts/Aller_Bd.ttf', 22)
day_font = ImageFont.truetype(f'{project_location}/fonts/Roboto-Black.ttf', 18)
icon_font = ImageFont.truetype(f'{project_location}/fonts/Roboto-Regular.ttf', 16)
date_font = ImageFont.truetype(f'{project_location}/fonts/Roboto-Bold.ttf', 14)
font = ImageFont.truetype(f'{project_location}/fonts/Roboto-Regular.ttf', 12)
small_font = ImageFont.truetype(f'{project_location}/fonts/ElecSign.ttf', 8)
smallest_font = ImageFont.truetype(f'{project_location}/fonts/ElecSign.ttf', 7)

# define weekday text
weekday = date.today()
day_name = date.strftime(weekday, '%A')
day_month = date.strftime(weekday, '%-d %B')

# format the summary texts for today
current_conditions = textwrap.fill(current_conditions, 19, max_lines=4)

# draw today's name on left side
draw.text((3, 3), day_name, inky_display.BLACK, day_font)

# draw today's date on left side below today's name
day_date = day_month
draw.text((3, 25), day_date, inky_display.BLACK, date_font)

#draw current temperature to right of day name and date. C and F
draw.text((105, 8), current_temp, inky_display.BLACK, temp_font)
draw.text((105, 34),current_temp_F, inky_display.BLACK, font)

# draw today's high and low temps on left side below date
draw.text((3, 44), temps_today, inky_display.BLACK, date_font)

# draw the current summary and conditions on the left side of the screen
draw.text((3, 60), current_conditions, inky_display.BLACK, font)

#draw a line to separate out the additional data
draw.line((119, 49, 119, 104),2, 4)

# draw dewpoint and wind data on lower right
draw.text((124, 51), wind_desc, inky_display.BLACK, font)
draw.text((124, 64), wind, inky_display.BLACK, font)
draw.text((124, 77), line3, inky_display.BLACK, font)
draw.text((124, 90), pressure, inky_display.BLACK, font)

# Dictionary to store our icons
icons = {}

# iterate through a list of the the weather icon file names
for icon in os.listdir(f'{project_location}/weather_icons/'):
    # build a list of the split file name's components
    icon_filename = icon.split('.')
    # use PIL module to id and open the current image file in the for loop
    icon_image = Image.open(f'{project_location}/weather_icons/{icon}')
    # assign the opened image file to the filename key in the dictionary {icons}
    # this key is the bit of the filename before the '.'
    icons[icon_filename[0]] = icon_image

# Draw the current weather icon using the current icon code as the key to
# the dictionary of images we've just created
if icon_code is not None:
    img.paste(icons[icon_code], (145, 2))


# # set up the image to push it
inky_display.set_image(img)
inky_display.set_border(inky_display.YELLOW)

# # push it all to the screen
inky_display.show()