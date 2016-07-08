# Use a NES-controller with your Raspberry Pi
I tried to connect a NES-controller with my Raspberry Pi which turned out to be pretty easy due to the fact that other persons figured out how NES-controllers work: my code is just the python3 implementation of the logic behind [some C code](http://forum.arduino.cc/index.php?topic=8481.0) written for the Arduino-platform, so thank you kind stranger 


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



