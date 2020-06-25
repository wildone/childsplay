# Child's Play

This is a project I created to keep my son occupied in my study while I work.

The concept is simple, get a raspberri pi, hook it up to old screen, wireless keyboard, mouse and a speaker.

#Let each tap of key or mouse click: 
* to change the colour of the screen, 
* print the key name,
* say out loud the character
* play music while infractions are happening
* stop music after 10 seconds
* resume music at next contact  

I used following as the original idea [Original Idea](https://willhaley.com/blog/fullscreen-raspberry-pi-app-tft/) and spent a lot of time stuffing around with Alsa (sound driver) and just ended up using command line tools to do all sounds as it all worked that way. 

#When you finish with Raspberry setup this you will know how to:
* create raspberry pi image using provided tools, see download section for this
* configure sound to use headphone jack
* disable all shortcuts in lightdm including how to unmap Alt+Tab which seems to be a special combo (hardcoded) 
* auto login with default pi users
* auto run a python application after login  
* how to use espeak to speak aloud text
* how to play music using omxplayer

#When you read the Python code you will learn how to:
* how to create a GUI app using Tkinter, which was very easy to use mind you
* make a pet project in a hurry
* run OS sub-processes on threads, this is uses to run omxplayer and espeak
* use multi processing with queues
* make classes with functions
* bind to all keyboard and mouse events
* change color of the screen
* use random to select things from array
* do timeouts for operations 

 
#What you need to do this
* Raspberry PI, something with HDMI and Headphones Jack and a USB power source
* SD Card 8GB
* Speaker and a cable to connect it to your RPI
* A screen, anything will do
* keyboard and mouse, wireless is better

#Downloads
* [SD Card Formatter](https://www.sdcard.org/downloads/formatter/eula_windows/SDCardFormatterv5_WinEN.zip)
* [Raspbarrian OS](https://downloads.raspberrypi.org/raspios_lite_armhf_latest)
* [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)

#Scripts

* install.sh - install all dependecies
* watch.sh - wait for app.py to be changed to reload the LightDM


#App

app.py - main app that will run full screen

#Process

1. Get your Pi setup
2. info folder `/home/pi` copy
    * app.py
    * config folde
    * music folder
    * install.sh
    * watch.sh
3. run `./install.sh`
4. create song.mp3 in `music` folder
5. reboot

