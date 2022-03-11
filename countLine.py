import adc
import time
import RPi.GPIO as GPIO
import board
import busio
from adafruit_ht16k33 import segments

#### SETUP 7 segment display ######

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)

# Clear the display.
display.fill(0)

display.print(0)
##### END SETUP ####

tripped_time_sec = 0
is_tripped = False
tripped_time_sec_exit = 0
is_tripped_exit = False
EXIT_LED = 17

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(EXIT_LED, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

def show_count():
  global count
  display.fill(0)
  display.print(count)

def light_on():
  print("light up!!!!!!!!!!!!!!!!!!!")
  GPIO.output(4, GPIO.HIGH) # Turn on

def light_off():
  print("light off??????")
  GPIO.output(4, GPIO.LOW) # Turn on

def exit_light_on():
  print("light up!!!!!!!!!!!!!!!!!!!")
  GPIO.output(EXIT_LED, GPIO.HIGH) # Turn on


def exit_light_off():
  print("light off??????")
  GPIO.output(EXIT_LED, GPIO.LOW) # Turn on



count = 0

def entered_line():
  light_on()
  global count
  count = count + 1
  print("count=" + str(count))
  show_count()

def exited_line():
  exit_light_on()
  global count
  count = count - 1
  show_count()

def check_entrance():
    global is_tripped
    global tripped_time_sec
    voltage = adc.get_adc(0)
    print("ADC Channel 0:", round(voltage, 2), "V")
    if(voltage < 2.3):
     # see if tripped for more than 2 seconds
     if(is_tripped):
       tripped_time_sec = tripped_time_sec + time.time()
       if(tripped_time_sec > 2):
         entered_line()
         # Reset is_tripped so we don't count same person multiple times
         is_tripped = False
     else:
       tripped_time_sec = 0
       is_tripped = True
    # else not tripped (not dropped below 2.3v
    else:
     tripped_time_sec = 0
     is_tripped = False
     light_off()


def check_exit():
    global is_tripped_exit
    global tripped_time_sec_exit
    voltage = adc.get_adc(1)
    print("ADC Channel 1:", round(voltage, 2), "V")
    if(voltage < 2.3):
     # see if tripped for more than 2 seconds
     if(is_tripped_exit):
       tripped_time_sec_exit = tripped_time_sec_exit + time.time()
       if(tripped_time_sec_exit > 2):
         exited_line()
         # Reset flag so we don't count the same person twice
         is_tripped_exit = False
     else:
       tripped_time_sec_exit = 0
       is_tripped_exit = True
    # else not tripped (not dropped below 2.3v
    else:
     tripped_time_sec_exit = 0
     is_tripped_exit = False
     exit_light_off()

try:
# Loop continually to check sensors
  while True:
    check_entrance()
    check_exit()
    time.sleep(0.2)

except KeyboardInterrupt:
  GPIO.cleanup()

