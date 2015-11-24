import time
import rtmidi
import random

midiout = {}
buttons = list(range(51, 35, -1))
color_dict = {
    'red':13,
    'orange':25,
    'yellow':37,
    'ygreen':49,
    'green':61,
    'cyan':73,
    'blue':85,
    'lylac':97,
    'magenta':109,
    'white':121,
    'cyanbright':127
}
colors = color_dict.values()
colors.sort()

def p(a,c):
    for i in buttons:
        midiout.send_message([a,i, c])
        
script = """
activate
tell application "System Events" to keystroke "%s"
"""

def runcommand(s):
    from subprocess import Popen, PIPE

    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(s)

import string
    
def echo((nums, ts), n):
    print nums
    action, button, vel = nums
    color = random.choice(colors)
    midiout.send_message([146, button, color])

    if action == 146 and (button >= 84 and button <= 99):
        key = string.letters[button - 84]
        runcommand(script % key)

    if action == 146 and button == 48:
        p(146, 0)
    elif action == 146 and button == 36:
        p(146, 121)
    elif action == 146 and button == 40:
        p(146, random.choice(colors))

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

midiin = rtmidi.MidiIn()
midiin.set_callback(echo)

if 'Midi Fighter Spectra' in available_ports:
    midiout.open_port(available_ports.index('Midi Fighter Spectra'))
    midiin.open_port(available_ports.index('Midi Fighter Spectra'))    
else:
    midiout.open_virtual_port("My virtual output")

p(146, 0)

raw_input()
