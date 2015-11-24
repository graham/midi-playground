import time
import rtmidi
import random

midiout = rtmidi.MidiOut()
midiin = rtmidi.MidiIn()
available_ports = midiout.get_ports()

midiout.open_port(available_ports.index('Midi Fighter Spectra'))
midiin.open_port(available_ports.index('Midi Fighter Spectra'))    

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

def rbutton():
    return random.choice(buttons)

def clear():
    for i in buttons:
        midiout.send_message([146, i, 0])

def pop():
    for i in buttons:
        midiout.send_message([146, i, rcolor()])

def roll():
    while True:
        pop()
        time.sleep(0.05)

def p(a,c):
    for i in buttons:
        midiout.send_message([a,i,c])

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

def bottom_on(bid):
    set_bottom(bid, 127)

def bottom_off(bid):
    set_bottom(bid, 1)

def set_bottom(bid, bright):
    midiout.send_message([147, bid, ])
    
def set_button(bid, color, bright=0, gate=None, pulse=None):
    midiout.send_message([147, bid, 18 + bright])
    midiout.send_message([146, bid, color])

    if gate:
        midiout.send_message([147, bid, 34+gate])
    if pulse:
        midiout.send_message([147, bid, 42+pulse])

def fader(bid):
    color = rcolor()
    for i in range(0, 16):
        for j in range(0, 2):
            yield set_button(bid, color, 15 - i)
    yield set_button(bid, 0, gate=0, pulse=0)


def echo((nums, ts), n):
    action, button, vel = nums
    if action == 146:
        funcs.append( fader(button) )
    elif action == 130:
        pass

midiin.set_callback(echo)
funcs = []

while True:
    time.sleep(0.025)
    keep = []
    for i in funcs:
        try:
            i.next()
            keep.append(i)
        except:
            keep.append(fader(rbutton()))

    funcs = keep

    
