# Connecting a Raspberry Pi to an original NES-controller
I tried to connect a NES-controller to my raspberry pi which turned out to be pretty easy due to the fact that other persons figured out how a NES-controller works: my code is the python3 implementation of the logic of a C-programm written for the Arduino-platform given at the following link: http://forum.arduino.cc/index.php?topic=8481.0 

# Pinout
Just connect the pins directly with the NES-controller, no electrical-engineering degree required
``` 
  ___________ 
 /           |
/      0V    |
|  5V  CLOCK |
|  x   LATCH |
|  x   DATA  |
|____________|
```
# Warning 
The NES-controller originally operates with 5 Volts but since the Raspberry only handles a maximum of 3.3 V input-voltage, I'd recommend you to stick with the 3.3 V in case you don't want to destroy your Raspberry Pi.

