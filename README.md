# Use a NES-controller with your Raspberry Pi
I've tried to connect a NES-controller with my Raspberry Pi (I used the B-revision of the first model) which turned out to be pretty easy due to the fact that other persons figured out how NES-controllers work: my code is just the python3 implementation of the logic behind [some C code](http://forum.arduino.cc/index.php?topic=8481.0) written for the Arduino-platform, so thanks to the person who wrote this gem.

**Note:** The contents of this repository are licensed under a BSD 3-clause license.


## Connect the controller with your GPIO pins
Just connect the pins directly with the NES-controller, no electrical-engineering degree required.
Here's the pinout:
``` 
  ___________ 
 /           |
/      0V    |
|  5V  CLOCK |
|  x   LATCH |
|  x   DATA  |
|____________|
```
Warning: The NES-controller originally operates with 5 Volts but since the Raspberry only handles a maximum of 3.3 V input-voltage, I'd recommend you to stick with the 3.3 V in case you don't want to destroy your Raspberry Pi (If you gave 5 V input to your NES-controller, it'd ouput 5V and potentially kill your Raspberry.)

![Image](https://cloud.githubusercontent.com/assets/20270187/16710403/fe80800a-462c-11e6-8d20-03cd5cbd9162.jpg)

## Usage (Python 3.x and 2.x)
**Note:** Although the code was originally designed to work with python 3, it should be perfectly fine to run it with python 2 (for the ```debug_print_controller_state()``` function and the debug mode the module checks the used version, since python 2.x uses ```raw_input()``` insted of ```input()``` and uses ```iteritems()``` instead of ```items()```. Besides that, there were no other modifications necessary for python 3.x/2.x compatibility).

You can convince yourself that it's quite straightforward to use nesctrl by looking at ```example.py ```.

### Method 1: import nesctrl to your project
Just ```import nesctrl```. It depends on the built-in python-modules ```time```,  ```collections``` and ```sys```. Furthermore, it depends on the  ```RPi-GPIO```-module which comes pre-installed with the current Raspian-Jesse and Wheezy releases for the Raspberry Pi so you shouldn't have to care about it.

With the nesctrl module imported, the first thing you have to do is to call the function ```nesctrl.setup(clock, latch, data) ``` once to 'initialize' the controller, where the parameters are the numbers of the corresponding gpio pins you're using (following the Broadcom gpio numbering scheme). 

Then you can call ```nesctrl.read_controller_state()``` whenever you want to read the state of your NES-controller. This function returns an ordered dictionary where the keys are strings describing the buttons of the NES-controller and the values are ```True``` if the button is pressed or ``` False``` if its not pressed:

```{"A": True, "B": False, "SELECT": False, "START": False, "UP": True, "DOWN": False, "LEFT": False, "RIGHT": False}``` (In this example, the 'A' and 'UP' buttons are pressed).

Before terminating your program, It's good practice to clean the used GPIO-pins by calling ``` nesctrl.cleanup()```.

Furthermore, it's perfectly possible to call the ```nesctrl.debug_print_pressed_buttons(controller_state)``` function which prints the pressed buttons, where ```controller_state``` is the dictionary returned by ```nesctrl.read_controller_state()```.

### Method 2: run nesctrl.py directly (entering the debug mode)
If you call the nesctrl.py script directly instead of importing it to your own code, you enter a 'debug mode' - a simple command line inteface which first asks which pins you've specified for  ```CLOCK```, ```LATCH``` and ```DATA```and which subsequentially outputs the pressed buttons of your controller forevermore. Quit the debug mode by pressing ``` ctrl-c```.


## Todo
- add support for 2 controllers
- add armv6 and c versions
- merge the python3/2 version into one **(Done!)**
- add docstrings etc **(Done, could be improved though)**.
- check if all ```time.sleep()``` calls are really necessary or could be easily ommited without causing problems **(Done!)**
- get rid of the necissity for the declaration of global variables (CLOCK, LATCH, DATA), pass them as function params instead **(Done!)**
- add a python2 implementation **(Done!)**
- find alternative for ugly for-loop at line 78 **(Done!)**
