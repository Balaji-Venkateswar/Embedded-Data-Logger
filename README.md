# Embedded-Data-Logger
The PI-Trokli development system has been used to implement an embedded data logger in this project. 
The PI-Trokli system has been manipulated using Python code and the specific libraries associated with it. 
The ultrasonic ranging module within the PI-Trokli system is used to acquire the data. Some basic functionalities like data collection, visualizing it numerically and graphically on Seven segment display and Matrix Led Display (MLD) has been implemented in section 2.1. The update rate functionality has been implemented in section 2.2. Further functionalities like “System pause and restart”, “Data archiving” and “Scrolling through collected values” has been implemented in section 2.3. Finally, auto-calibration functionality has been provided to the system in section 2.4 to scale the measured values in the PI-Trokli system.


# section 2.1.py
In this section of code, the ultrasonic sensor is activated and measurements are taken. The measurements are scaled to a value between 0% to 100%. Then, the measurements are displayed on the seven-segment display with a sleep duration of 1 second. The measurements are also continuously displayed on the Matrix Led Display (MLD) such that old measurements are moved out of the MLD as new measurements are displayed.

# section 2.2.py
In this section of code , the update rate functionality is provided. As the update rate is increased, the time duration between each data collection by the ultrasonic ranging module in the PI-Trokli system will increase. The update rate is increased by pressing Up Button in PI-Trokli. For each press, the update rate will increase by one second. If the update rate reaches greater than 9 second, then the update rate will be reset to one second.

# section 2.3.py
In this section of code, a buffer has been created to store hundred values of scaled_values. From 101th reading, the first value will be removed from the array and all the other values will get shifted to their previous index positions. And the 101th value will be stored in the 99th index. The pause and restart functionality to data collection of the ultrasonic module is also given using the Left button in the PI-Trokli system. If pressed once, the system will get paused and if pressed again, the system will restart collecting data. In addition, once the system is paused, the right button can be used to scroll through the buffer and display the corresponding values on 7SD and previous 7 values on MLD.

# section 2.4.py
In this section, auto-calibration functionality is provided if the down button pressed. By pressing the down button, the system will go into calibration mode and take 10 measurements within 5 seconds. During the calibration, the buzzer is activated by setting it as HIGH and after 5 seconds setting it as LOW. The scaling is done using alpha * techo. (Where alpha = 100/ (mean of 10 techoreadings)).

All the tasks were executed successfully. It gave an understanding of the basic functionalities while executing each task. I hope this knowledge could help me during further developments of the system.
