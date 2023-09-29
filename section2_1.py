# Import necessary libraries and modules
import RPi.GPIO as GPIO
import time
from Adafruit_LED_Backpack import SevenSegment
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Define the serial interface (SPI)
serial = spi(port=0, device=1, gpio=noop())
# Defining a max7219 device
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)

# Define a segment object
segment_7SD = SevenSegment.SevenSegment(address=0x70)
# Initialise the 7SD
segment_7SD.begin()

# Define GPIO numbering mode
GPIO.setmode(GPIO.BCM)
# Define pins of Trigger and Echo pin
PinTrigger = 16
PinEcho = 12
# Defining input and output
GPIO.setup(PinTrigger, GPIO.OUT)
GPIO.setup(PinEcho, GPIO.IN)
# Set Trigger pin to false and wait for 1 sec.
GPIO.output(PinTrigger, False)
print('Initialising Sensor \n')
time.sleep(1)


def measurement(PinTrigger, PinEcho):
    GPIO.output(PinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(PinTrigger, False)
    while GPIO.input(PinEcho) == 0:
        pulse_start = time.time()               # Setting the initial start time
    while GPIO.input(PinEcho) == 1:
        pulse_end = time.time()                 # Noting down the end time once PinEcho becomes High
    time_duration = pulse_end - pulse_start
    return time_duration


def ssddisplay(dist):
    str_measurement = str(round(dist, 1))
    segment_7SD.clear()                         # Clearing the 7SD before writing the new value
    # Writing with a for-loop
    for i in range(len(str_measurement) - 1):
        if len(str_measurement) == 5:
            if not i == 3:
                segment_7SD.set_digit(i, str_measurement[i])
            else:
                segment_7SD.set_digit(i, str_measurement[i + 1])

        if len(str_measurement) == 4:
            segment_7SD.set_digit(0, 0)         # Always setting the 0th index position as zero since the distance has no hundred's column
            if not i == 2:
                segment_7SD.set_digit(i + 1, str_measurement[i])
            else:
                segment_7SD.set_digit(i + 1, str_measurement[i + 1])

        if len(str_measurement) == 3:
            segment_7SD.set_digit(0, 0)
            segment_7SD.set_digit(1, 0)         # Always setting the 0th and 1st index position as zero since the distance has no hundred's and ten's column
            if not i == 1:
                segment_7SD.set_digit(i + 2, str_measurement[i])
            else:
                segment_7SD.set_digit(i + 2, str_measurement[i + 1])

    segment_7SD.set_decimal(2, True)            # To display the decimal point at the 2nd index position
    segment_7SD.write_display()                 # Writing the scaled_value on the 7SD
    time.sleep(1)


height = [0,0,0,0,0,0,0,0]                      # Creating a zeros list with 8 values
loop = 0
while True:
    with canvas(device) as draw:                                # Syntax to use the draw functionality and display on MLD
        pulse_duration = measurement(PinTrigger, PinEcho)       # Calling the measurement function by passing PinTrigger and PinEcho
        print("Pulse_duration:",pulse_duration,"secs")
        scaled_value = (pulse_duration * 100)/0.013                 # Scaling the pulse_duration and scaling factor is assumed as 13ms
        print("Scaled_value:", scaled_value, "cm")
        ssddisplay(scaled_value)                                    # Calling the ssddisplay function by passing distance parameter
        if loop<8:
            height[loop] = int(round(7 * (scaled_value / 100)))        # Scaling the measured value to less than 8 in order to display on MLD
            draw.point([loop,7 - height[loop]], fill="white")
        else:
            for j in range(0,7):
                height[j] = height[j+1]                         # Shifting the index values in the 'height' list to create a moving graph
                draw.point([j, 7 - height[j]], fill="white")
            height[7] = int(round(7 * (scaled_value / 100)))
            draw.point([7, 7 - height[7]], fill="white")
        print("Height list:", height,'\n')
        loop += 1




