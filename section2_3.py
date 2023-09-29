# Import necessary libraries and modules
import RPi.GPIO as GPIO
import time
import numpy as np
from Adafruit_LED_Backpack import SevenSegment
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas


serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)

segment_7SD = SevenSegment.SevenSegment(address=0x70)
segment_7SD.begin()
segment_7SD.clear()
segment_7SD.write_display()

GPIO.setmode(GPIO.BCM)
PinTrigger = 16
PinEcho = 12
PinLeft = 25
PinRight = 19
PinUp = 26
Input_pins = [PinEcho,PinLeft,PinRight, PinUp]
GPIO.setup(PinTrigger, GPIO.OUT)
GPIO.setup(Input_pins, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.output(PinTrigger, False)
print('Initialising Sensor \n')
time.sleep(1)


def measurement(PinTrigger, PinEcho,c):
    if c % 2 == 0:                                  # to check whether the left button is pressed or not in order to operate the ultrasonic sensor
        GPIO.output(PinTrigger, True)
        time.sleep(0.00001)
        GPIO.output(PinTrigger, False)
        while GPIO.input(PinEcho) == 0:
            pulse_start = time.time()
        while GPIO.input(PinEcho) == 1:
            pulse_end = time.time()
        time_duration = pulse_end - pulse_start
        return time_duration
    else:
        print("System is paused \n \n")
        return 0


def ssddisplay(dist):
    str_measurement = str(round(dist, 1))
    segment_7SD.clear()
    for i in range(len(str_measurement) - 1):
        if len(str_measurement) == 5:
            if not i == 3:
                segment_7SD.set_digit(i, str_measurement[i])
            else:
                segment_7SD.set_digit(i, str_measurement[i + 1])

        if len(str_measurement) == 4:
            segment_7SD.set_digit(0, 0)
            if not i == 2:
                segment_7SD.set_digit(i + 1, str_measurement[i])
            else:
                segment_7SD.set_digit(i + 1, str_measurement[i + 1])

        if len(str_measurement) == 3:
            segment_7SD.set_digit(0, 0)
            segment_7SD.set_digit(1, 0)
            if not i == 1:
                segment_7SD.set_digit(i + 2, str_measurement[i])
            else:
                segment_7SD.set_digit(i + 2, str_measurement[i + 1])

    segment_7SD.set_decimal(2, True)
    segment_7SD.write_display()

def counter(channel):               # function to check whether the left button is pressed or not inorder to pause or restart the system
    global c
    c += 1

def update_rate (channel):          # function to change the update rate value
    global d
    d += 1

def scroll(channel):                # function to scroll and display the values on 7SD and MLD
    global c, readings, measured_count
    if c % 2 == 0:
        print("CANNOT SCROLL NOW. PLEASE PAUSE THE SYSTEM TO SCROLL \n\n")
    else:
        if readings < 0:
            print(" CANNOT SCROLL FURTHER. YOU HAVE REACHED THE END OF THE BUFFER \n")
        else:
            a = readings
            with canvas(device) as draw:
                ssddisplay(buffer[0,readings])
                for k in range(0,8):
                    if a < 0:
                        break
                    draw.point([7-k ,7-buffer[1,a]], fill="white")
                    a -= 1
            readings -= 1


GPIO.add_event_detect(PinLeft,GPIO.RISING,callback = counter)
GPIO.add_event_detect(PinRight,GPIO.RISING,callback = scroll)
GPIO.add_event_detect(PinUp,GPIO.RISING,callback = update_rate)

buffer = np.zeros([2,100])              # Creation of an two dimensional array to store the distance and MLD graph values
measured_count = -1
readings = -1
c = 0
d = 1
loop = 0
while True:
    pulse_duration = measurement(PinTrigger, PinEcho,c)         # passing 'c' parameter additionally to the function
    if pulse_duration > 0:
        segment_7SD.clear()
        segment_7SD.write_display()
        device.clear()
        scaled_value = (pulse_duration * 100)/0.013
        print("Scaled_value:", scaled_value, "cm")

        if loop > 99:
            readings = 99
            for j in range(0, 99):
                buffer[0,j] = buffer[0,j + 1]
                buffer[1,j] = buffer[1,j+1]
            buffer[0,99] = scaled_value
            buffer[1,99] = int(round(7 * (scaled_value / 100)))

        else:
            readings = measured_count
            buffer[0,loop] = scaled_value
            buffer[1,loop] = int(round(7 * (scaled_value / 100)))
            measured_count += 1
            readings += 1
        loop += 1

        if d > 9:
            d = 1                                   # Variable 'd' is reset to '1' if the Up button is pressed 10th time
            print("UPDATE RATE RESET")
        print("The current update rate is ", d, "secs \n")
    time.sleep(d)                                   # Sleep duration or update rate is changed based upon the value of 'd'







