# RPIFanController

## Multiple fan controller

This tool try to provide a two channel fan controller based on pin 13 and 19. It works with a 100Hz PWM signal (still using SW PWM and more than 8kHz is harder to go, so i decided to sacrify fan efficiency for lower fan noise). For the moment the channel are in parallel, but in future will be more indipendent.

The main fan is on pin 19, and the secondary are on pin 13.

The fans must not be directly connected to RP pins, the configuration is designed for a single quadrant chopper with a NPN or a N-Channel mosfet:

![Chopper configuration](https://github.com/94-psy/RPIFanController/blob/master/chopper.png "Chopper configuration")

## Installation:

`wget https://raw.githubusercontent.com/94-psy/RPIFanController/master/install.sh && chmod +x install.sh && ./install.sh && rm install.sh `
