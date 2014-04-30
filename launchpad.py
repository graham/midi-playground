import time
import rtmidi
import random

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

note_on = [0x90, 00, 60] # channel 1, middle C, velocity 112

buffer1 = lambda: midiout.send_message([144, 0, 49])
buffer0 = lambda: midiout.send_message([144, 0, 52])

def full(value):
    for col in range(0, 8):
        for row in range(0, 8):
            loc = (16 * row) + col
            midiout.send_message([0x90, loc, value])
sleep = lambda: time.sleep(0.05)

buffer1()

full(12)
buffer0()
sleep()

full(63)
buffer1()
sleep()

full(15)
buffer0()
sleep()

full(60)
buffer1()
sleep()

full(12)
buffer0()
sleep()

saved = []

def responder(pack, other):
    keys, time = pack
    chan, key, vel = keys
    if vel == 0:
        if key not in saved:
            midiout.send_message([0x90, key, 12])
    elif vel == 127:
        c = random.choice([63,15,60])
        if c == 15:
            saved.append(key)
        midiout.send_message([0x90, key, c])

midiin = rtmidi.MidiIn()
midiin.open_port(0)
midiin.set_callback(responder)

raw_input()
