import os
import pathlib
import requests
import textwrap
from datetime import date, timedelta, datetime
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
import glob
import textwrap
import logging

from dotenv import load_dotenv
load_dotenv()

# a programme to display today's weather and tomorrow
# on the inky_display

# set lat/long for location
# put your longitude and latitude here in decimal degrees
LOCATION = os.getenv("LOCATION")

# Get an api key for climacell here: https://www.climacell.co/weather-api/
APIKEY = os.getenv("APIKEY")

# Want to use fahrenheit? set to true.
FAHRENHEIT = os.getenv("FAHRENHEIT")

# set the colour of the phat: black, red or yellow
INKY_COLOUR = os.getenv("INKY_COLOUR")

# set the colour of the phat: black, red or yellow
inky_display = InkyPHAT(INKY_COLOUR)
# rotate inky so the plugs are on the top. comment to unflip.
inky_display.rotation = 90

# import our fonts
current_dir = pathlib.Path(__file__).parent
tempFont = ImageFont.truetype(f'{current_dir}/fonts/Aller_Bd.ttf', 22)
dayFont = ImageFont.truetype(
    f'{current_dir}/fonts/Roboto-Black.ttf', 18)
iconFont = ImageFont.truetype(
    f'{current_dir}/fonts/Roboto-Medium.ttf', 16)
dateFont = ImageFont.truetype(
    f'{current_dir}/fonts/Roboto-Bold.ttf', 14)
font = ImageFont.truetype(
    f'{current_dir}/fonts/Roboto-Regular.ttf', 12)
smallFont = ImageFont.truetype(f'{current_dir}/fonts/ElecSign.ttf', 8)
smallestFont = ImageFont.truetype(
    f'{current_dir}/fonts/ElecSign.ttf', 7)


weatherCode = {
    0: "unknown",
    1000: "clear",
    1001: "cloudy",
    1100: "mostly clear",
    1101: "partly cloudy",
    1102: "mostly cloudy",
    2000: "fog",
    2100: "light fog",  # no icon
    3001: "wind",
    3002: "strong wind",  # no icon
    4000: "drizzle",  # no icon
    4001: "rain",
    4200: "light rain",  # no icon
    4201: "heavy rain",  # no icon
    5000: "snow",
    5001: "sleet",
    5100: "light snow",  # no icon
    5101: "heavy snow",  # no icon
    6000: "freezing drizzle",  # no icon
    6001: "freezing rain",  # no icon
    6200: "light freezing rain",  # no icon
    6201: "heavy freezing rain",  # no icon
    7000: "ice pellets",  # no icon
    7101: "heavy ice pellets",  # no icon
    7102: "light ice pellets",  # no icon
    8000: "thunderstorm"  # no icon
}

# Get data from Climacell

# fields for climacell:
# https://docs.climacell.co/reference/data-layers-overview#field-availability

fields = ['temperature', 'temperatureMin', 'temperatureMax', 'weatherCode', 'humidity', 'epaIndex',
          'pressureSurfaceLevel', 'windDirection', 'windGust', 'windSpeed', 'dewPoint']
queryParams = {'location': LOCATION,
               'fields': ','.join(fields), 'timesteps': '1m'}
r = requests.get('https://data.climacell.co/v4/timelines', params=queryParams,
                 headers={'apikey': APIKEY})
if r.status_code == 200:
    today = r.json()['data']['timelines'][0]['intervals'][0]['values']

    currentTemp = today['temperature']
    relativeHumidity = today['humidity']
    windSpeed = today['windSpeed']
    windGust = today['windGust']
    windBearing = today['windDirection']
    pressure = today['pressureSurfaceLevel']
    dewPoint = today['dewPoint']
    epaIndex = today['epaIndex']

    upcoming_conditions = weatherCode[today['weatherCode']]
    iconDesc = weatherCode[today['weatherCode']]
    highTemp = today['temperatureMax']
    lowTemp = today['temperatureMin']

else:
    logging.critical(f"Error: {r.status_code}: {r.json()['message']}")
    # If you find an error, print it to the display.
    img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)
    draw.text(
        (3, 3), f'Error @{datetime.now().strftime("%H:%M:%S")}', inky_display.BLACK, dayFont)
    draw.text((3, 25), textwrap.fill(
        r.json()['message'], width=30), inky_display.BLACK, dateFont)
    inky_display.set_image(img)
    inky_display.set_border(inky_display.YELLOW)
    inky_display.show()
    quit()


def toF(C): return round((1.8 * C) + 32)


if FAHRENHEIT:
    temp = str(toF(currentTemp)) + '°'
    altTemp = str(round(currentTemp)) + 'C'
    highTemp = toF(highTemp)
    lowTemp = toF(lowTemp)
    dewPoint = toF(dewPoint)
else:
    temp = round(currentTemp)
    temp = str(temp) + '°'
    altTemp = str(toF(currentTemp)) + 'F'
    highTemp = round(highTemp)
    lowTemp = round(lowTemp)
    dewPoint = round(dewPoint)

tempsToday = 'Low ' + str(lowTemp) + ' High ' + str(highTemp)
dewPoint = ' dew ' + str(dewPoint) + 'F' if FAHRENHEIT else 'C'

# format today's variables to current temp and high and low temps for the day

pressure = round(pressure)
pressure = str(pressure) + ' hPa'

# convert the wind bearing to a compass direction using a tuple of 16 compass points
# and format the other wind information. We need to do windBearing  modulo 360 first
# to allow for 0 degree bearing.
windDir = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N')
windBearing = windBearing % 360
windIndex = round(windBearing / 45)
compassDir = windDir[windIndex]
windSpeed = round(windSpeed)
windGust = round(windGust)
gust = ' gust ' + str(windGust)

# determine Beaufort scale number and wind description from wind speed
if windSpeed < 1:
    windDesc = 'Calm'
    Beaufort = - 0
elif (windSpeed >= 1 and windSpeed <= 3):
    windDesc = 'Light Air'
    Beaufort = 1
elif windSpeed <= 7:
    windDesc = 'Light Breeze'
    Beaufort = 2
elif windSpeed <= 12:
    windDesc = 'Gentle Breeze'
    Beaufort = 3
elif windSpeed <= 18:
    windDesc = 'Moderate Breeze'
    Beaufort = 4
elif windSpeed <= 24:
    windDesc = 'Fresh Breeze'
    Beaufort = 5
elif windSpeed <= 31:
    windDesc = 'Strong Breeze'
    Beaufort = 6
elif windSpeed <= 38:
    windDesc = 'Near Gale'
    Beaufort = 7
elif windSpeed <= 46:
    windDesc = 'Gale'
    Beaufort = 8
elif windSpeed <= 54:
    windDesc = 'Strong Gale'
    Beaufort = 9
elif windSpeed <= 63:
    windDesc = 'Storm'
    Beaufort = 10
elif windSpeed <= 72:
    windDesc = 'Violent Storm'
    Beaufort = 11
else:
    windDesc = 'Hurricane'
    Beaufort = 12

# prepare info for  line about the wind speed and Beaufort scale
wind = str(windSpeed) + ' ' + compassDir + gust

# prepare info for line 3 which is dewpoint and  wind gusts
line3 = 'Bft.' + str(Beaufort) + ' ' + dewPoint

# This imports three classes from PIL that we'll need, creates a new blank
# image, img, that is the width and height of the Inky pHAT display,
# and then creates a drawing canvas, draw, to which we can draw text and graphics
img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# define weekday text
weekday = date.today()
day_Name = date.strftime(weekday, '%A')
day_month = date.strftime(weekday, '%-d %B')

# format the summary texts for today
currentCondFormatted = textwrap.fill(upcoming_conditions, 19, max_lines=4)

# draw today's name on left side
draw.text((3, 3), day_Name, inky_display.BLACK, dayFont)

# draw today's date on left side below today's name
dayDate = day_month
draw.text((3, 25), dayDate, inky_display.BLACK, dateFont)

# draw current temperature to right of day name and date. C and F
draw.text((105, 8), temp, inky_display.BLACK, tempFont)
draw.text((105, 34), altTemp, inky_display.BLACK, font)

# draw today's high and low temps on left side below date
draw.text((3, 44), tempsToday, inky_display.BLACK, dateFont)

# draw the current summary and conditions on the left side of the screen
draw.text((3, 60), currentCondFormatted, inky_display.BLACK, font)
draw.text((3, 76), f'AQI: {epaIndex}',
          inky_display.BLACK if epaIndex < 100 else inky_display.RED, font)

# draw a line to separate out the additional data
draw.line((119, 49, 119, 104), 2, 4)

# draw dewpoint and wind data on lower right
draw.text((124, 51), windDesc, inky_display.BLACK, font)
draw.text((124, 64), wind, inky_display.BLACK, font)
draw.text((124, 77), line3, inky_display.BLACK, font)
draw.text((124, 90), pressure, inky_display.BLACK, font)

# Dictionary to store our icons
icons = {}

# Load our icon image files and generate masks
for icon in glob.glob(f'{current_dir}/weather-icons/icon-*.png'):
    # format the file name down to the text we need
    # example: 'icon-fog.png' becomes 'fog'
    icon_name = icon.split('icon-')[1].replace('.png', '')
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image


try:
    # Draw the current weather icon
    if iconDesc is not None:
        img.paste(icons[iconDesc], (145, 2))
except:
    logging.warning('No icon found for weather pattern')

# set up the image to push it
inky_display.set_image(img)

if INKY_COLOUR == 'red':
    inky_display.set_border(inky_display.RED)
elif INKY_COLOUR == 'yellow':
    inky_display.set_border(inky_display.YELLOW)
else:
    inky_display.set_border(inky_display.BLACK)

# push it all to the screen
inky_display.show()
