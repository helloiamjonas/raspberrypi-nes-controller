# Use a NES-controller with your Raspberry Pi (work in progress)
I tried to connect a NES-controller with my Raspberry Pi (I used the B-revision of the first model) which turned out to be pretty easy due to the fact that other persons figured out how NES-controllers work: my code is just the python3 implementation of the logic behind [some C code](http://forum.arduino.cc/index.php?topic=8481.0) written for the Arduino-platform, so thank you kind stranger(s). 


# Connect the controller with your GPIO pins
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
Warning: The NES-controller originally operates with 5 Volts but since the Raspberry only handles a maximum of 3.3 V input-voltage, I'd recommend you to stick with the 3.3 V in case you don't want to destroy your Raspberry Pi (If you'd input 5V to your NES-controller, it will ouput 5V and potentially kill your Raspberry.)

# Usage
Using nesctrl.py is easy. 

Just ```import nesctrl```. It depends on the modules ```RPi-GPIO``` and ```time``` which come pre-installed with the current Raspian-Jesse for the Raspberry Pi so you shouldn't have to care about it. Chose your Version (python2 or 3)

Before being able to read the state of the controller, you have to  ``` nesctrl.setup(CLOCK, LATCH, DATA) ``` once (where the parameters are the pin numbers (following the Broadcom pin numbering scheme) you are using for the  given purposes) 

Then you can call ```nesctrl.read_controller_state()``` whenever you want to read the state of your NES-controller. This function returns a list with 8 elements (one for every button; the same button always has the same index which can therefore be used to identify the pressed button). The element is 0 if the button is pressed, and 1 if it is not pressed 

Additionally, you might want to call the ``` nesctrl.print_buttons(pressed_buttons)``` functions, where pressed_buttons is the mentioned list.

Before terminating your program, It's good practice to clean the used GPIO-pins by calling ``` nesctrl.clean()```.


