#!/bin/bash
wget https://raw.githubusercontent.com/94-psy/RPIFanController/master/FanController.py -O ~/.FanController.py
sudo wget https://raw.githubusercontent.com/94-psy/RPIFanController/master/fanctrl.service -O /lib/systemd/system/fanctrl.service
sudo systemctl enable fanctrl.service
sudo systemctl restart fanctrl.service
