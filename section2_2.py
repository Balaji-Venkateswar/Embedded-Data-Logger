# Import necessary libraries and modules
import RPi.GPIO as GPIO
import time
from Adafruit_LED_Backpack import SevenSegment
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)

# Define a segment object
segment_7SD = SevenSegment.SevenSegment(address=0x70)
# Initialise the 7SD
segment_7SD.begin()

GPIO.setmode(GPIO.BCM)
PinTrigger = 16
PinEcho = 12
PinButtonUp = 26                    # Here: Up button is introduced to change the update rate or sleep duration
inputs = [PinEcho,PinButtonUp]
GPIO.setup(PinTrigger, GPIO.OUT)
GPIO.setup(inputs, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.output(PinTrigger, False)
print('Initialising Sensor \n')
time.sleep(1)


def measurement(PinTrigger, PinEcho):
    GPIO.output(PinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(PinTrigger, False)
    while GPIO.input(PinEcho) == 0:
        pulse_start = time.time()
    while GPIO.input(PinEcho) == 1:
        pulse_end = time.time()
    time_duration = pulse_end - pulse_start
    return time_duration


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

d = 1
def update_rate(channel):    # 'counter' function will get called once 'Up button' is pressed
    global d             # The variable 'c' is declared global as it needs to be taken outside the function and to avoid the local variable issue
    d = d + 1            # Incrementing the value of 'c' to change the update rate as Up button is pressed

GPIO.add_event_detect(PinButtonUp,GPIO.RISING,callback = update_rate)    # add_event_detect method is used to continuously monitor whether Up button is High or Low
height = [0,0,0,0,0,0,0,0]
loop = 0
while True:
    pulse_duration = measurement(PinTrigger, PinEcho)
    scaled_value = (pulse_duration * 100)/0.013
    print("Scaled_value:", scaled_value, "cm")
    ssddisplay(scaled_value)
    with canvas(device) as draw:
        if loop < 8:
            height[loop] = int(round(7 * (scaled_value / 100)))
            draw.point([loop, 7 - height[loop]], fill="white")
        else:
            for j in range(0, 7):
                height[j] = height[j + 1]
                draw.point([j, 7 - height[j]], fill="white")
            height[7] = int(round(7 * (scaled_value / 100)))
            draw.point([7, 7 - height[7]], fill="white")
    loop += 1

    if d > 9:
        d = 1                            # Variable 'd' is reset to '1' if the Up button is pressed 10th time
        print("UPDATE RATE RESET")
    print("The current update rate is ",d,"secs \n")
    time.sleep(d)                        # Sleep duration or update rate is changed based upon the value of 'd'




