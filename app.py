#-*- coding: utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import StringVar
import tkinter.font as font
import random
from evdev import InputDevice, categorize, ecodes

from threading import Thread
import os
import subprocess

import multiprocessing as mp
import collections

Msg = collections.namedtuple('Msg', ['text'])

from omxplayer.player import OMXPlayer #runs from the popcornmix omxplayer wrapper at https://github.com/popcornmix/omxplayerhttps://github.com/popcornmix/omxplayer and https://python-omxplayer-wrapper.readthedocs.io/en/latest/)
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)

timeout = 10000

playSong = True
sayThings = True

after_id = None
song = None
talk = None
#set num lock
dev = InputDevice('/dev/input/event0') # your keyboard device
dev.set_led(ecodes.LED_NUML, 1)

APLAY_PARAMS = "--device=hw:1,0"
NAME = "Arkadi"

MUSIC = ['song.mp3']

COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4']

def donothing():
    pass


def restart():
    # Run a new iteration of the current script, providing any command line args from the current iteration.
    os.execv(__file__, sys.argv)

def session_end():
    label.config(bg='black')
    label.config(fg="white")
    labelText.set("Hello {name}!".format(name = NAME))
    if playSong:
        song.pause()


def right(s, amount):
    return s[-amount:]

def keypress(event):
    global after_id
    if after_id is not None:
        root.after_cancel(after_id)

    after_id = root.after(10000, session_end)

    label.config(fg="black")

    labelText.set(event.keysym.upper())
    label.config(bg=random.choice(COLORS))

    if playSong:
        song.play()

    if sayThings:
        talk.say(event.char)




def labelprep(event):
    event.widget.focus_set()  # give keyboard focus to the label
    event.widget.bind('<Key>', keypress)


class FullScreenApp(object):
    padding=3
    dimensions="{0}x{1}+0+0"

    def __init__(self, master, **kwargs):
        self.master=master
        width=master.winfo_screenwidth()-self.padding
        height=master.winfo_screenheight()-self.padding
        master.geometry(self.dimensions.format(width, height))

        frame = Frame(master)
        frame.config(cursor='none')
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)

        myFont = font.Font(family='Courier', size=80, weight='bold')
        global label
        label = Label(frame, textvariable=labelText, font=myFont)
        #label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label.config(height=height, width=width)
        label.config(bg='black')
        label.config(fg="white")

        label.pack(expand=YES, fill=BOTH)


    def pressed(self):
        print("clicked!")

    def mouseClickButton1(event):
        print('clicked at', event.x, event.y)


class Song(Thread):

    def __init__(self, f, *args, **kwargs):
        self.__file = f
        self.__player = None
        Thread.__init__(self, *args, **kwargs)
        self.start()

    def pause(self):
        if self.__player is not None:
            self.__player.pause()

    def stop(self):
        if self.__player is not None:
            self.__player.pause()

    def set_position(self, set_position):
        if self.__player is not None:
            self.__player.set_position(set_position)

    def play(self):
        if self.__player is not None:
            self.__player.play()

    def run(self):
        print("Song: Init")
        if self.__file is not None:
            self.__file_path = Path(self.__file)
            self.__player = OMXPlayer(self.__file_path, args='--loop')
            self.pause()
            self.set_position(0)
        print("Song: Ready")


class Talk(Thread):

    def __init__(self, f, *args, **kwargs):
        self.queue = mp.Queue()
        self.max = 3
        self.count = 0
        self.__text = f
        self.__is_ready = True
        self.__is_busy = False
        Thread.__init__(self, *args, **kwargs)
        self.start()

    def say(self, text):
        if text is not "":
            msg = Msg(text)
            if self.count < self.max:
                print("Talk: Add to queue " + msg.text)
                self.queue.put(msg)
                self.count += 1
            if self.count >= self.max:
                print("Queue is full")


    def dispatch(self, msg):
        text = msg.text

        print("Talk: Saying [" + text + "]")
        os.system("espeak \"{text}\" --stdout | aplay {device}".format(text = text, device = APLAY_PARAMS))
        print("Talk: Done Saying [" + text + "]")
        self.count -= 1



    def run(self):
        print("Talk: Init")
        while True:
            msg = self.queue.get()

            print("Talk: Get from queue " + msg.text)
            self.dispatch(msg)




root=tk.Tk()
root.wm_attributes('-fullscreen','true')

root.protocol('WM_DELETE_WINDOW',donothing)

root.bind_all("<Any-KeyPress>", keypress)
root.bind_all("<Any-ButtonPress>", keypress)

labelText = StringVar()
labelText.set("Hello Arkadi!")
label = None

if sayThings:
    talk = Talk("")

if playSong:
    song = Song("./music/" + random.choice(MUSIC))

app=FullScreenApp(root)

root.mainloop()
