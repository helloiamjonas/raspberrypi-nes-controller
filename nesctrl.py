#!/usr/bin/python3

""" ˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
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

TODO: Is it really necessary to wati 1/10th of a second after every read-cycle?

˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
"""

import RPi.GPIO as gpio
import time
import sys

# necessary to prepare the controller for the first time
# -> only sideeffects, no return values 
def setup():
    # Use Broadcom gpio numbering scheme
    gpio.setmode(gpio.BCM)

    gpio.setup(CLOCK, gpio.OUT)
    gpio.setup(LATCH, gpio.OUT)
    gpio.setup(DATA, gpio.IN)

    gpio.output(CLOCK, gpio.HIGH)
    gpio.output(LATCH, gpio.HIGH)

# assumes that the global variables CLOCK, LATCH and DATA are set
# -> returns list of pressed buttons
def read_controller_state():
    pressed_buttons = []

    gpio.output(CLOCK, gpio.LOW)
    gpio.output(LATCH, gpio.LOW)

    # state of the first button
    gpio.output(LATCH, gpio.HIGH)
    time.sleep(20**-6)  # wait for 2 µs
    gpio.output(LATCH, gpio.LOW)
    
    pressed_buttons.append(gpio.input(DATA))
    
    # state of remaining 7 buttons
    for i in range(7):
        gpio.output(CLOCK, gpio.HIGH)
        time.sleep(20**-6)
        pressed_buttons.append(gpio.input(DATA))
        time.sleep(40**-6)
        gpio.output(CLOCK, gpio.LOW)
        
    return pressed_buttons


def cleanup():
    gpio.cleanup()



# (DEBUG-FUNCTION) assumes controller state array in original order
# -> prints names of pressed buttons and returns them
def print_buttons(pressed_buttons, noprint=False):
    button_dict = {0: "A", 1: "B", 2: "SELECT", 3:"START", 4:"UP", 5: "DOWN", 6: "LEFT", 7: "RIGHT"}
    output_string = "Buttons pressed: "
    zero_len = len(output_string)
    for i in range(8):
        if pressed_buttons[i] == 0:
            output_string += str(button_dict[i]) + " "
    
    # print 'None' if no btn pressed
    if len(output_string) == zero_len:
        output_string += "None"
        
    print(output_string)
    return output_string
          
# (DEBUG-FUNCTION)
def input_pins():
    print("Input your pins following the Broadcom Gpio numbering scheme")
    try:
        CLOCK = int(input("CLOCK: "))
        LATCH = int(input("LATCH: "))
        DATA = int(input("DATA: "))
        
        if CLOCK == LATCH or CLOCK == DATA or LATCH == DATA:
            raise ValueError
    
    # if the specified input is NaN or if two specified pins are the same -> ValueError 
    except ValueError:
        if str(input("Invalid pin number. Try again? (y/n) ")).lower() == "y":
            input_pins()
        else:
            sys.exit()    




# DEBUG-MODE if you call the script directly
if __name__ == "__main__":
    print("You entered the Debug-mode by calling the nesctrl.py script directly. It will output the controller state untill you "
          "interrupt the execution of the program  with ctrl-c.")
    
    # gpio pin definitions (following the bcm numbering scheme)
    CLOCK = 22
    LATCH = 17
    DATA = 4
    
    custom_pins = str(input("Use custom pin numbers? (y/n)"))
    if custom_pins.lower() == "y":
        input_pins()
    
    # initial setup, only required once
    setup()
    
    try: 
        while True:  
            pressed_buttons = read_controller_state()
            print(pressed_buttons)
            print_buttons(pressed_buttons)
            time.sleep(0.01) # wait for 1/100th of a second
    
    except KeyboardInterrupt:
        cleanup()
        print("\n Debug-mode terminated.")    
        sys.exit(0)
