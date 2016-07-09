# Use a NES-controller with your Raspberry Pi (work in progress)
I tried to connect a NES-controller with my Raspberry Pi (I used the B-revision of the first model) which turned out to be pretty easy due to the fact that other persons figured out how NES-controllers work: my code is just the python3 implementation of the logic behind [some C code](http://forum.arduino.cc/index.php?topic=8481.0) written for the Arduino-platform, so thank you kind stranger(s). 


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

## Usage
Using nesctrl.py is easy. 
### Python 3.x
Just ```import nesctrl```. It depends on the modules ```RPi-GPIO``` which comes pre-installed with the current Raspian-Jesse release for the Raspberry Pi (plus the built-in modules ```time``` and '''collections''') so you shouldn't have to care about it. 

Before being able to read the state of the controller, you have to  ``` nesctrl.setup() ``` once (first you have to specify the global constants CLOCK, LATCH and DATA (pin numbers you're using following the Broadcom numbering scheme)) 

Then you can call ```nesctrl.read_controller_state()``` whenever you want to read the state of your NES-controller. This function returns a list with 8 elements (one for every button; the same button always has the same index which can therefore be used to identify the pressed button). The element is 0 if the button is pressed, and 1 if it is not pressed 

Additionally, you might want to call the ``` nesctrl.print_buttons(pressed_buttons)``` functions, where pressed_buttons is the mentioned list.

Before terminating your program, It's good practice to clean the used GPIO-pins by calling ``` nesctrl.clean()```.

### Python 2.x
Not yet implemented
