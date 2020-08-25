#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

# Configuration
FAN1_PIN = 19  # BCM pin used to drive transistor's base
FAN2_PIN = 13 #Secondary fan
WAIT_TIME = 1  # [s] Time to wait between each refresh
FAN_MIN = 10  # [%] Fan minimum speed.
PWM_FREQ = 100  # [Hz] Change this value if fan has strange behavior

# Configurable temperature and fan speed steps
tempSteps = [30, 65]  # [°C]
speedSteps = [10, 100]  # [%]

# Fan speed will change only of the difference of temperature is higher than hysteresis
hyst = 1

# Setup GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN1_PIN, GPIO.OUT, initial=GPIO.LOW)
fan1 = GPIO.PWM(FAN1_PIN, PWM_FREQ)
fan1.start(0)
GPIO.setup(FAN2_PIN, GPIO.OUT, initial=GPIO.LOW)
fan2 = GPIO.PWM(FAN2_PIN, PWM_FREQ)
fan2.start(0)

i = 0
cpuTemp = 0
fanSpeed1 = 0
cpuTempOld = 0
fanSpeed1Old = 0

# We must set a speed value for each temperature step
if len(speedSteps) != len(tempSteps):
    print("Numbers of temp steps and speed steps are different")
    exit(0)

try:
    while 1:
        # Read CPU temperature
        cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
        cpuTemp = float(cpuTempFile.read()) / 1000
        cpuTempFile.close()

        # Calculate desired fan speed
        if abs(cpuTemp - cpuTempOld) > hyst:
            # Below first value, fan will run at min speed.
            if cpuTemp < tempSteps[0]:
                fanSpeed1 = speedSteps[0]
            # Above last value, fan will run at max speed
            elif cpuTemp >= tempSteps[len(tempSteps) - 1]:
                fanSpeed1 = speedSteps[len(tempSteps) - 1]
            # If temperature is between 2 steps, fan speed is calculated by linear interpolation
            else:
                for i in range(0, len(tempSteps) - 1):
                    if (cpuTemp >= tempSteps[i]) and (cpuTemp < tempSteps[i + 1]):
                        fanSpeed1 = round((speedSteps[i + 1] - speedSteps[i])
                                         / (tempSteps[i + 1] - tempSteps[i])
                                         * (cpuTemp - tempSteps[i])
                                         + speedSteps[i], 1)

            if fanSpeed1 != fanSpeed1Old:
                if (fanSpeed1 != fanSpeed1Old
                        and (fanSpeed1 >= FAN_MIN or fanSpeed1 == 0)):
                    fan1.ChangeDutyCycle(fanSpeed1)
                    fan2.ChangeDutyCycle(fanSpeed1)
                    fanSpeed1Old = fanSpeed1
            cpuTempOld = cpuTemp

        # Wait until next refresh
        time.sleep(WAIT_TIME)


# If a keyboard interrupt occurs (ctrl + c), the GPIO is set to 0 and the program exits.
except KeyboardInterrupt:
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
