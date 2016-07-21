#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" ˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
By Jonas U.

The following code is based on the Arduino-version written in C on "http://forum.arduino.cc/index.php?topic=8481.0"  
(-> so this person did the actual work of figuring out how a NES-controller works, thank you kind stranger).

I remind you: this code comes with ABSOLUTELY NO WARRANTY, I am not responsible for any broken NES-controllers
or Raspberry-Pies (pun intended) or any other possible damage caused by this script.

Pinout of the NES-Controller:
  __________ 
 /          .
/      0V   . 
. 5V   CLOCK.
. x    LATCH.
. x    DATA .
.___________.  

(WARNING: USE 3.3V INSTEAD OF 5V IF YOU DON'T WANT TO DESTROY YOUR RASPBERRY PI)

˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
"""
__author__ = "Jonas U."
__credits__ = ["This guy: http://forum.arduino.cc/index.php?topic=8481.0"]
__license__ = "BSD 3-clause"

# built-in
import time
import sys
import collections
# preinstalled on raspian wheezy/jessie
import RPi.GPIO as gpio

# the globals modified with the setup function
CLOCK, LATCH, DATA = 0, 0, 0

def setup(clock, latch, data):
    """ necessary to prepare the controller for the first time
    -> only sideeffects, no return values """ 
    # in order to avoid having to set the params for every function
    global CLOCK
    global LATCH
    global DATA
    CLOCK, LATCH, DATA = clock, latch, data
    # Use Broadcom gpio numbering scheme
    gpio.setmode(gpio.BCM)

    gpio.setup(CLOCK, gpio.OUT)
    gpio.setup(LATCH, gpio.OUT)
    gpio.setup(DATA, gpio.IN)

    gpio.output(CLOCK, gpio.HIGH)
    gpio.output(LATCH, gpio.HIGH)


def read_controller_state():
    """ assumes that the global variables CLOCK, LATCH and DATA are set
    -> returns list of pressed buttons """
    # setting things up
    pressed_buttons = []
    gpio.output(CLOCK, gpio.LOW)
    gpio.output(LATCH, gpio.LOW)

    # recieve state of the first button
    gpio.output(LATCH, gpio.HIGH)
    time.sleep(20**-6)  # wait for 2 µs
    gpio.output(LATCH, gpio.LOW)
    pressed_buttons.append(not gpio.input(DATA)) # 'not' since the input is 0 if the button is pressed
    
    # recieve state of remaining 7 buttons
    for i in range(7):
        gpio.output(CLOCK, gpio.HIGH)
        time.sleep(20**-6)
        pressed_buttons.append(not gpio.input(DATA))
        gpio.output(CLOCK, gpio.LOW)
    
    # 'transform' the pressed_buttons list into an easier to use dict:
    # Note: the controller_state dict has to be ordered because the position of a element (True for pressed, False for not pressed)
    # in the pressed_buttons list determines the button it is associated with (e.g element at pos. 0 associated with "A" etc.) 
    controller_state = collections.OrderedDict([("A",False),  ("B",False), ("SELECT",False), ("START",False), ("UP",False), ("DOWN",False), ("LEFT",False), ("RIGHT",False)])
    for i, button in enumerate(controller_state):
        controller_state[button] = pressed_buttons[i]
        
    return controller_state  
            
  
def cleanup():
    """ kind of self explanatory: clean gpio-registers 
    -> not return value, only sideeffects """ 
    gpio.cleanup()


def debug_print_buttons(controller_state):
    """ (DEBUG-FUNCTION) assumes controller state array in original order
    -> prints names of pressed buttons and returns them """
    output_string = "Button(s) pressed:"
    no_button_pressed = True
    # for python 2.x, items() is iteritems()
    if sys.version_info[0] < 3:
        for button, is_pressed in controller_state.iteritems():
            if is_pressed:
                no_button_pressed = False
                output_string += " " + button
    # python 3.x uses items()
    else:
        for button, is_pressed in controller_state.items():
            if is_pressed:
                no_button_pressed = False
                output_string += " " + button
    
    if not no_button_pressed:
        print(output_string)
    else:
        print(output_string + " None")
       
             
def debug_input_pins():
    """ (DEBUG-FUNCTION) asks user of debug mode for pins to input """
    print("Input your pins following the Broadcom gpio numbering scheme")
    try:
        # python 2.x uses raw_input()
        if sys.version_info[0] < 3:
            CLOCK = int(raw_input("CLOCK: "))
            LATCH = int(raw_input("LATCH: "))
            DATA = int(raw_input("DATA: "))
        
        # python 3.x uses input()
        else:
            CLOCK = int(input("CLOCK: "))
            LATCH = int(input("LATCH: "))
            DATA = int(input("DATA: "))
        
        # rudimentary 'input validation'      
        if (CLOCK == LATCH or CLOCK == DATA or LATCH == DATA) or (CLOCK <= 0 or LATCH <= 0 or DATA <= 0):
            raise ValueError
      
        return {"CLOCK": CLOCK, "LATCH": LATCH, "DATA": DATA}

    # if the specified input is NaN or if two specified pins are the same or < 0 -> ValueError 
    except ValueError:
	# use raw_input() for python 2.x
        if sys.version_info[0] < 3:
            if str(raw_input("Invalid pin number. Try again? (y/n) ")).lower() == "y":
                debug_input_pins()
       # python 3.x uses input()
        else:
            if str(input("Invalid pin number. Try again? (y/n) ")).lower() == "y":
                debug_input_pins()
            else:
                sys.exit(1)    




# DEBUG-MODE if you call the script directly
if __name__ == "__main__":
  
    print("You entered the Debug-mode by calling the nesctrl.py script directly. It will output the controller state untill you "
          "interrupt the execution of the program  with ctrl-c.")
    
    # python 2.x
    if sys.version_info[0] < 3:
        custom_pins = str(raw_input("Use custom pin numbers? (y/n)"))
    # pyhton 3.x
   
    else:
        custom_pins = str(input("Use custom pin numbers? (y/n)"))
    if custom_pins.lower() == "y":
        # use user-defined pins
        custom_pins = debug_input_pins()
        setup(custom_pins["CLOCK"], custom_pins["LATCH"], custom_pins["DATA"])
    else:
        # use my defualt pins
        CLOCK, LATCH, DATA= 22, 17, 4
        setup(CLOCK, LATCH, DATA)
    
    try: 
        while True:  
            controller_state = read_controller_state()
            debug_print_buttons(controller_state)
            time.sleep(0.01) # wait for 1/100th of a second
    
    except KeyboardInterrupt:
        cleanup()
        print("\n Debug-mode terminated.")    
        sys.exit(0)
        
