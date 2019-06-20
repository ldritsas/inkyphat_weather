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

# set the colour of the phat: black, red or yellow
inky_display = InkyPHAT('your_colour')

# set lat/long for location
LOCATION = #put your longitude and latittude here in decimal degrees
UNITS = '?' #specify the units you want your results in here, see the Dark Sky API docs page for details 

# set Darksky API Key
APIKEY= '?' # put your Dark Sky API key here. Get one at https://darksky.net/dev

# Get data from DarkSky
with forecast (APIKEY, *LOCATION, units=UNITS) as location:
    # today
    currentTemp = location['currently']['temperature']
    upcoming_conditions = location['minutely']['summary']
    relativeHumidity = location['currently']['humidity']
    highTemp = location['daily']['data'][0]['temperatureHigh']
    lowTemp = location['daily']['data'][0]['temperatureLow']
    iconDesc = location['currently']['icon']
  
    # tomorrow 
    summary2 = location['daily']['data'][1]['summary']
    iconDesc2 = location['daily']['data'][1]['icon']
    highTemp2 = location['daily']['data'][1]['temperatureHigh']
    lowTemp2 = location['daily']['data'][1]['temperatureLow']

# format today's variables, current temp and high and low temps for the day
temp = '{0:.0f}'.format(currentTemp) + '°'
currentTempF = round((1.8 * currentTemp) + 32)
tempF = str(currentTempF) + 'F'
tempsToday = 'High ' + '{0:.0f}'.format(highTemp) + ' Low ' + '{0:.0f}'.format(lowTemp)
  
# format tomorrow's variables 
tempsDay2 = 'High ' + '{0:.0f}'.format(highTemp2) + ' Low ' + '{0:.0f}'.format(lowTemp2)

# Create a new blank image, img, of type P 
# that is the width and height of the Inky pHAT display,
# then create a drawing canvas, draw, to which we can draw text and graphics
img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# import the fonts and set sizes
tempFont = ImageFont.truetype('fonts/Aller_Bd.ttf', 22)
dayFont = ImageFont.truetype('fonts/Roboto-Black.ttf', 18)
dateFont = ImageFont.truetype('fonts/Roboto-Bold.ttf', 14)
font = ImageFont.truetype('fonts/ElecSign.ttf', 10)
smallFont = ImageFont.truetype('fonts/ElecSign.ttf', 8)
smallestFont = ImageFont.truetype('fonts/ElecSign.ttf', 7)

# define weekday text
weekday = date.today()
day_Name = date.strftime(weekday, '%A')
day_month_year = date.strftime(weekday, '%-d %B %y')

weekday2 = datetime.date.today() + datetime.timedelta(days=1)
day2 = date.strftime(weekday2, '%A')

# format the summary texts for today and tomorrow
currentCondFormatted = textwrap.fill(upcoming_conditions, 16)
summary2Formatted = textwrap.fill(summary2, 18)
iconFormatted = textwrap.fill(iconDesc, 7)

# draw some lines to boix out tomorrow's forecast
draw.line((118, 50, 118, 104),2, 4)
draw.line((118, 50, 212, 50),2, 4)

# draw today's name on top left side
draw.text((3, 3), day_Name, inky_display.BLACK, dayFont)

# draw today's date on left side below today's name
dayDate = day_month_year
draw.text((3, 25), dayDate, inky_display.BLACK, dateFont)

#draw current temperature to right of day name and date
#in both Celcius and Farhenhiet for old-timers
draw.text((105, 8), temp, inky_display.BLACK, tempFont)
draw.text((105, 34), tempF, inky_display.BLACK, font)

# draw today's high and low temps to center on left side below date
w, h = dateFont.getsize(tempsToday)
x_temps = (inky_display.WIDTH / 4) - (w / 2)
draw.text((x_temps, 45), tempsToday, inky_display.BLACK, font)

# draw the current summary and conditions on the left side of the screen
draw.text((3, 60), currentCondFormatted, inky_display.BLACK, smallFont)

# draw tomorrow's forecast in lower right box
draw.text((125, 55), day2, inky_display.BLACK, font)
draw.text((125, 66), tempsDay2, inky_display.BLACK, smallFont)
draw.text((125, 77), summary2Formatted, inky_display.BLACK, smallestFont)

# prepare to draw the icon on the upper right side of the screen
# Dictionary to store the icons
icons = {}

# build the dictionary 'icons'
for icon in glob.glob('weather-icons/icon-*.png'):
    # format the file name down to the text we need
    # example: 'icon-fog.png' becomes 'fog'
    # and gets put in the libary 
    icon_name = icon.split('icon-')[1].replace('.png', '')
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image

# Draw the current weather icon top in top right
if iconDesc is not None:
    img.paste(icons[iconDesc], (145, 2))        
else:
    draw.text((140, 10), '?', inky_display.YELLOW, dayFont)


# set up the image to push it
inky_display.set_image(img)
inky_display.set_border(inky_display.YELLOW)

# push it all to the screen
inky_display.show()
