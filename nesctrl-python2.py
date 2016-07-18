#!/usr/bin/python
# -*- coding: utf-8 -*-
""" ˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
THIS IS THE PYTHON2 VERSION OF NESCTRL

By github.com/helloiamjonas

The following code is based on the Arduino-version written in C on http://forum.arduino.cc/index.php?topic=8481.0  
(-> so this person did the actual work, thank you kind stranger)
I remind you: this code comes with ABSOLUTELY NO WARRANTY, I don't want to be responsible for any broken NES-controllers
Feel free to use the code in any way as long your use of it doesn't harm any living organism.


Pinout of the NES-Controller:
  __________ 
 /          .
/      OV   . 
. 5V   CLOCK.
. x    LATCH.
. x    DATA .
.___________.  

(WARNING: USE 3.3V INSTEAD OF 5V IF YOU DON'T WANT TO DESTROY YOUR RASPBERRY PI)

˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
"""

import RPi.GPIO as gpio
import time
import collections

# the globals modified with the setup function
CLOCK, LATCH, DATA = 0, 0, 0

def setup(clock, latch, data):
    """ 
    Note: 
        It's necessary to call this function one time before being able to call any other function of this module. 
        (It sets up the specified pins and declares the globals CLOCK, LATCH and DATA to make the pins numbers 
        accesible by other functions of this module) 
    
    Args: 
        clock (int):  The pin number (following the broadcom numbering scheme) of the pin connected with the clock pin  
        latch (int): The pin number of the pin connected with the latch pin
        data (int); The pin number of the pin connected with the data pin
        
    Returns: 
        bool: True if init was successfull, False otherwise.
    """
    # in order to avoid having to set the params for every functions
    try:
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
      
        return True
    
    except:
        return False

def read_controller_state():
    """ 
    Note: 
        Assumes the globals CLOCK, LATCH and DATA are set and the mode of the pins 
        are set properly (both accomplished by calling the setup() function)
    Args:
        None
      
    Returns: 
        dict: contains the state of the pressed buttons, where a key (string) corresponds to the name of a button
        of the NES controller in uppercase letters and its value (bool) indicates whether it was pressed (True) or not (False)
    """
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
        time.sleep(40**-6)
        gpio.output(CLOCK, gpio.LOW)
    
    # 'process' the pressed_buttons list into an easier to use dict:
    # Note: the controller_state dict has to be ordered because the position of a element (True for pressed, False for not pressed)
    # in the pressed_buttons list determines the button it is associated with (e.g element at pos. 0 associated with "A" etc.) 
    controller_state = collections.OrderedDict([("A",False),  ("B",False), ("SELECT",False), ("START",False), ("UP",False), ("DOWN",False), ("LEFT",False), ("RIGHT",False)])
  
    for i, button in enumerate(controller_state):
        controller_state[button] = pressed_buttons[i]
        
    return controller_state  
            
  
def cleanup():
    """ 
    Note: It's good practice to call this as soon as you don't need to read the buttons of your NES-controller anymore
    to free the GPIO pins.
    
    Args:
        None
        
    Returns: 
        bool: True if cleaned the pin succesfully, False otherwise.
      
    """ 
    try:
        gpio.cleanup()
        return True
    
    except:
        return False

def debug_print_buttons(controller_state):
    """
    Note: 
        Assumes the globals CLOCK, LATCH and DATA are set and the mode of the pins 
        are set properly (both accomplished by calling the setup() function
        
        (DEBUG-FUNCTION) assumes controller state array in original order and prints the presse buttons 
    
    Args: 
        controller_state (dict): The dict by the read_controller_state() function
        
    Returns:
        string: The sentence 'Buttons(s) pressed: ' followed by the name of the pressed buttons or 'None' 
   """
      
    output_string = "Button(s) pressed:"
    no_button_pressed = True
    for button, is_pressed in controller_state.iteritems():  # iteritems() instead of item in python2
        if is_pressed:
            no_button_pressed = False
            output_string += " " + button
    
    if not no_button_pressed:
        print(output_string)
        return output_string
    else:
        print(output_string + " None")
        return output_string
       
             
def debug_input_pins():
    """ 
    Note: 
        (DEBUG-FUNCTION) asks user of debug mode for pins to input 
    
    Args: 
        None
    
    Returns: 
        None
    """
    print("Input your pins following the Broadcom gpio numbering scheme")
    try:
        CLOCK = int(input("CLOCK: "))
        LATCH = int(input("LATCH: "))
        DATA = int(input("DATA: "))
        # rudimentary input validation
        if (CLOCK == LATCH or CLOCK == DATA or LATCH == DATA) or (CLOCK <= 0 or LATCH <= 0 or DATA <= 0):
            raise ValueError
      
        return {"CLOCK": CLOCK, "LATCH": LATCH, "DATA": DATA}

    # if the specified input is NaN or if two specified pins are the same or < 0 -> ValueError 
    except ValueError:
        if str(raw_input("Invalid pin number. Try again? (y/n) ")).lower() == "y":    # use raw_input for python2
            input_pins()
        else:
            sys.exit(1)    
            
            
            
            
# DEBUG-MODE if you call the script directly
if __name__ == "__main__":
    import sys

    print("You entered the Debug-mode by calling the nesctrl.py script directly. It will output the controller state untill you "
          "interrupt the execution of the program  with ctrl-c.")
    
    custom_pins = str(raw_input("Use custom pin numbers? (y/n)"))       # use raw_input for python2
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
        
