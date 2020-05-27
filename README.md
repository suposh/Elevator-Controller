# Elevator-Controller
## Hardware used
* ESP32 DevkitC (4 Mb)(Rev 1)
* Motor Driver Module -> l293d
* IR Sensor

This project is a simplistic Implementation of a  Elevator Controllerbuilt for ESP32.
Driver function for Motor Controller Module re-written for timer based fall-back system, in case, the IR sensor fails to register the door open/close event.
