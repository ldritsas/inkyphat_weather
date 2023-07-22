# inkyphat_weather
Python3 code to display current weather conditions on an Pimoroni Inky pHAT eInk screen using the [OpenWeather API](https://openweathermap.org/) My installation is on a Raspberry Pi Zero W running headless. The screen will display the date, expected temperatures for the day, including the barometric pressure, dewpoint, wind speed, gusts and Beaufort scale numbers.

Note that this is not yet updated to the One Call API 3.0 I will do this soon.

## UK units
Because I live in the UK, the units are a bit of a mix. Here we talk about temperature in Celcius, but windspeed in miles-per-hour. I've also incuded the temperature in Farhenheit units as well. The wind speed and directon are provided, then  gust speeds. 'Bft.' refers to the Beaufort scale, and the wind description is also taken from the Beaufort Scale, this helps me plan activities on the water. 'dew' refers the dewpoint, which I prefer to relative humidity.

## Acknowledgements
- I took inspiration from Alan Cunningham's [Inky pHAT Dark Sky weather display](https://github.com/AlanCunningham/inkyphat-darksky-weather-display/) 
- The icons are based on Adam Whitcroft’s [Climacons](http://adamwhitcroft.com/climacons/)
  - I used Gimp to convert the Climacon images to the custom pallet that the inky pHAT requires and to make the sun icons yellow, which is a neat effect and why I bought a yellow Inky pHAT from [Pimoroni](https://shop.pimoroni.com/products/inky-phat)
- If you are new to the Inky pHAT, you should read the Pimoroni pages about it [Getting Started with Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)

## Dependencies and requirements
- You will need to get an API key from OpenWeather and know your longitude and latitude
- You will also need:
- [Inky pHAT library](https://github.com/pimoroni/inky)
- [Pillow](https://pillow.readthedocs.io/en/stable/) imaging library
- and the two resource folders, 'fonts' and 'weather_icons' need to be in the same directory as the main program.

## Tips
- On your own system you will need to edit the loction of the resource files (the fonts and icons) depending on where you put them). I found that I needed absolute links in the code to make it work properly.
- I suggest creating a cron job that refreshes the screen every 10 minutes with new data. This is a lot simpler than it sounds, check [here](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/) for guidance. I did not see any benefit to more frequent requests. OpenWeather updats every 10 minutes.


### open_weather_today.py
![image](weather_today.png)

## License

GNU General Public License v3.0
