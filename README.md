# Use a NES-controller with your Raspberry Pi
I tried to connect a NES-controller to my raspberry pi which turned out to be pretty easy due to the fact that other persons figured out how NES-controllers work: my code isdjust the python3 implementation of the logic behing a C-programm written for the Arduino-platform given at the following link: http://forum.arduino.cc/index.php?topic=8481.0 

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
Warning: The NES-controller originally operates with 5 Volts but since the Raspberry only handles a maximum of 3.3 V input-voltage, I'd recommend you to stick with the 3.3 V in case you don't want to destroy your Raspberry Pi (If you'd input 5V to your NES-controller, it will ouput 5V and potentially kill your Raspberry.)



