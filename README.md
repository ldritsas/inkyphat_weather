# inkyphat_weather
Python3 Code to display current and near-term weather conditions on an Pimoroni Inky pHAT eInk screen Using the [Dark Sky API](https://darksky.net/dev/) and Lukas Kubis's Python wrapper [darkskylib](https://github.com/lukaskubis/darkskylib/). My installation is on a Raspberry Pi Zero W running headless on my kitchen wall. 

## Acknowledgements
- I took inspiration from Alan Cunningham's [Inky pHAT Dark Sky weather display](https://github.com/AlanCunningham/inkyphat-darksky-weather-display/) 
- The icons are based on Adam Whitcroft’s [Climacons](http://adamwhitcroft.com/climacons/)
  - I used Gimp to convert the Climacon images to the custom pallet that the inky pHAT requires.
- If you are new to the Inky pHAT, you should read the Pimoroni pages about it [Getting Started with Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)

## Dependencies and requirements
- You will need to get an API key from Dark Sky and know your longitude and latitude
- [Inky pHAT library](https://github.com/pimoroni/inky)
- [darkyskylib](https://github.com/lukaskubis/darkskylib)
- [Pillow](https://pillow.readthedocs.io/en/stable/) imaging library

## Tips
- On your own system you may need to adjust the loction of the resource files (the fonts and icons, depending on where you put them). I found that I needed absolute links n the code to make it work properly.
- I suggest creating a cron job that refreshes the screen every 15 minutes with new data. This is a lot simpler than it sounds, check [here](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/) for guidance. I did not see any benefit to more frequent requests.

## Example
![Image](inky-pHAT.png)


