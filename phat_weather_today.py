# a programme to display today's weather and tomorrow
# on the inky_display using Lukas Kubis's Python wrapper
# for the Dark Sky API https://github.com/lukaskubis/darkskylib 

import glob
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
import datetime
from datetime import date, timedelta
from darksky import forecast
import textwrap

# set the colour of the phat
inky_display = InkyPHAT('yellow')

# set lat/long for location and the units you need
LOCATION = 'your location here lat/long
UNITS = 'your preferred units, check Dark Sky for code'

# set Darksky API Key
APIKEY= 'your API key here'

# Get data from DarkSky
with forecast (APIKEY, *LOCATION, units=UNITS) as location:
    # today
    currentTemp = location['currently']['temperature']
    upcoming_conditions = location['minutely']['summary']
    relativeHumidity = location['currently']['humidity']
    dewPoint = location['currently']['dewPoint']
    windSpeed = location['currently']['windSpeed']
    windGust = location['currently']['windGust']
    windBearing = location['currently']['windBearing']
    pressure = location['currently']['pressure']
    highTemp = location['daily']['data'][0]['temperatureHigh']
    lowTemp = location['daily']['data'][0]['temperatureLow']
    iconDesc = location['currently']['icon']
  
# format today's variables to current temp and high and low temps for the day
temp = round(currentTemp)
temp = str(temp) + '°'
currentTempF = round((1.8 * currentTemp) + 32)
tempF = str(currentTempF) + 'F'
highTemp = round(highTemp)
lowTemp = round(lowTemp)
tempsToday =  'Low ' + str(lowTemp) + ' High ' + str(highTemp)  
dewPoint = round(dewPoint)
dewPoint = ' dew ' + str(dewPoint) + 'C'
pressure = round(pressure)
pressure = str(pressure) + ' hPa'

# convert the wind bearing to a compass direction using a tuple of 16 compass points
# and format the other wind information. We need to do windBearing  modulo 360 first
# to allow for 0 degree bearing.
windDir = ('N','NE','E','SE','S','SW','W','NW','N')
windBearing = windBearing % 360
windIndex = round(windBearing/ 45)
compassDir = windDir[windIndex]
windSpeed = round(windSpeed)
windGust = round(windGust)
gust = ' gust ' + str(windGust)

#determine Beaufort scale number and wind description from wind speed
if windSpeed < 1:
    windDesc = 'Calm'
    Beaufort =- 0
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


# tomorrow's variables 
# tempsDay2 = 'High ' + '{0:.0f}'.format(highTemp2) + ' Low ' + '{0:.0f}'.format(lowTemp2)

# This imports three classes from PIL that we'll need, creates a new blank
# image, img, that is the width and height of the Inky pHAT display,
# and then creates a drawing canvas, draw, to which we can draw text and graphics
img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# import our fonts
tempFont = ImageFont.truetype('/home/pi/weatherDisplay/fonts/Aller_Bd.ttf', 22)
dayFont = ImageFont.truetype('/home/pi/weatherDisplay/fonts/Roboto-Black.ttf', 18)
iconFont = ImageFont.truetype('/home/pi/weatherDisplay/fonts/Roboto-Medium.ttf', 16)
dateFont = ImageFont.truetype('/home/pi/weatherDisplay/fonts/Roboto-Bold.ttf', 14)
font = ImageFont.truetype('/home/pi/weatherDisplay/fonts/Roboto-Regular.ttf', 12)
smallFont = ImageFont.truetype('/home/pi/weatherDisplay/fonts/ElecSign.ttf', 8)
smallestFont = ImageFont.truetype('/home/pi/weatherDisplay/fonts/ElecSign.ttf', 7)

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

#draw current temperature to right of day name and date. C and F
draw.text((105, 8), temp, inky_display.BLACK, tempFont)
draw.text((105, 34), tempF, inky_display.BLACK, font)

# draw today's high and low temps on left side below date
draw.text((3, 44), tempsToday, inky_display.BLACK, dateFont)

# draw the current summary and conditions on the left side of the screen
draw.text((3, 60), currentCondFormatted, inky_display.BLACK, font)

#draw a line to separate out the additional data
draw.line((119, 49, 119, 104),2, 4)

# draw dewpoint and wind data on lower right
draw.text((124, 51), windDesc, inky_display.BLACK, font)
draw.text((124, 64), wind, inky_display.BLACK, font)
draw.text((124, 77), line3, inky_display.BLACK, font)
draw.text((124, 90), pressure, inky_display.BLACK, font)

# Dictionary to store our icons
icons = {}

# Load our icon image files and generate masks
for icon in glob.glob('/home/pi/weatherDisplay/weather-icons/icon-*.png'):
    # format the file name down to the text we need
    # example: 'icon-fog.png' becomes 'fog'
    icon_name = icon.split('icon-')[1].replace('.png', '')
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image

# Draw the current weather icon
if iconDesc is not None:
    img.paste(icons[iconDesc], (145, 2))        


# set up the image to push it
inky_display.set_image(img)
inky_display.set_border(inky_display.YELLOW)

# push it all to the screen
inky_display.show()
