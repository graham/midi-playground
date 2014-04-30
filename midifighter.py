import time
import rtmidi
import random

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
note_off = [0x80, 60, 0]
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)

buttons = list(range(51, 35, -1))
color_dict = {
    'off':0,
    'red':13,
    'redlow':19,
    'orange':25,
    'orangelow':31,
    'yellow':37,
    'yellowlow':43,
    'ygreen':49,
    'ygreenlow':55,
    'green':61,
    'green-low':67,
    'cyan':73,
    'cyanlow':79,
    'blue':85,
    'bluelow':91,
    'lylac':97,
    'lylaclow':103,
    'magenta':109,
    'magentalow':115,
    'white':121,
    'cyanbright':127
}
colors = color_dict.values()
colors.sort()

def choose_bank(id):
    midiout.send_message([147, id, 127])

def rcolor():
    return random.choice(colors)

def clear():
    for i in buttons:
        midiout.send_message([146, i, 0])

def pop():
    for i in buttons:
        midiout.send_message([146, i, rcolor()])

def roll():
    while True:
        pop()
        time.sleep(0.25)

def p(a,c):
    for i in buttons:
        midiout.send_message([a,i, c])

def waterfall():
    while True:
        color = random.choice(colors)
        for i in range(18, 34):
            p(147, i)
            p(146, color)
            time.sleep(0.025)

        for i in range(33, 17, -1):
            p(147, i)
            p(146, color)
            time.sleep(0.025)

        for i in range(16, 20):
            midiout.send_message([147, i, 127])
        time.sleep(0.2)
        for i in range(16, 20):
            midiout.send_message([147, i, 1])
