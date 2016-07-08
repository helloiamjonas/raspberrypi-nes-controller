#!/usr/bin/python3

""" ˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
By Jonas U.

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
    for i in range(8):
        gpio.output(CLOCK, gpio.HIGH)
        time.sleep(20**-6)
        pressed_buttons.append(gpio.input(DATA))
        time.sleep(40**-6)
        gpio.output(CLOCK, gpio.LOW)
        
    return pressed_buttons


# assumes controller state array in original order
# -> prints names of pressed buttons and returns them
def printButtons(pressed_buttons, noprint=False):
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
           
        

if __name__ == "__main__":
    # Pin definitions
    CLOCK = 22
    LATCH = 17
    DATA = 4
    setup()

    while True:
        try:
            pressed_buttons = read_controller_state()
            printButtons(pressed_buttons)
            time.sleep(0.01) # wait for 1/100th of a second
        except KeyboardInterrupt:
            print("Clean GPIO-Pins...")
            gpio.cleanup()
            sys.exit()
            
            
    
