# Use a NES-controller with your Raspberry Pi (work in progress)
I tried to connect a NES-controller with my Raspberry Pi (I used the B-revision of the first model) which turned out to be pretty easy due to the fact that other persons figured out how NES-controllers work: my code is just the python3 implementation of the logic behind [some C code](http://forum.arduino.cc/index.php?topic=8481.0) written for the Arduino-platform, so thanks to the person who wrote this gem.

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

## Usage (Python 3.x)

### Methdod I: import nesctrl to your project
Just ```import nesctrl```. It depends on the module ```RPi-GPIO``` which comes pre-installed with the current Raspian-Jesse and Wheezy releases for the Raspberry Pi (+ dependend on the built-in python-modules ```time``` and ```collections```) so you shouldn't have to care about it. 

With the nesctrl module imported, the first thing you have to do is to declare the global variables ```CLOCK```, ```LATCH``` and ```DATA``` and assign them to the corresponding gpio numbers you're using (following the Broadcom gpio numbering scheme). 
Before being able to read the state of the controller, you have to call``` nesctrl.setup() ``` once. 

Then you can call ```nesctrl.read_controller_state()``` whenever you want to read the state of your NES-controller. This function returns an ordered dictionary where the keys are strings describing the buttons of the NES-controller and the values are ```True``` if the button is pressed or ``` False``` if its not pressed:

```{"A": True, "B": False, "SELECT": False, "START": False, "UP": True, "DOWN": False, "LEFT": False, "RIGHT": False}``` (In this example, the 'A' and 'UP' buttons are pressed).

Before terminating your program, It's good practice to clean the used GPIO-pins by calling ``` nesctrl.cleanup()```.

Furthermore, it's perfectly possible to call the ```nesctrl.debug_print_pressed_buttons(controller_state)``` function which prints the pressed buttons, where ```controller_state``` is the dictionary returned by ```nesctrl.read_controller_state()```.

### Method II: run nesctrl.py directly 
If you call the nesctrl.py script directly instead of importing it to your own code, you enter a 'debug mode' - a simple command line inteface which first asks the pins you've specified for  ```CLOCK```, ```LATCH``` and ```DATA```and which subsequentially outputs the pressed buttons of your controller forevermore. Quit the debug mode by pressing ``` ctrl-c```.

Note: The Debug-mode also depends on the built-in module ```sys```.


## Usage (Python 2.x)
Not (yet) implemented.

## Todo
- add docstrings etc.
- check if all ```time.sleep()``` calls are really necessary or could be easily ommited without causing problems
- get rid of global variables, its kind of stupid
