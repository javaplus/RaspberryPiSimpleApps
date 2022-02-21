import adc
import time
import RPi.GPIO as GPIO


tripped_time_sec = 0
is_tripped = False
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

def light_on():
  print("light up!!!!!!!!!!!!!!!!!!!")  
  GPIO.output(5, GPIO.HIGH) # Turn on


def light_off():
  print("light off??????")  
  GPIO.output(5, GPIO.LOW) # Turn on


# Report the photoresistor  voltages to the terminal
try:
  while True:
    voltage = adc.get_adc(0)
    print("ADC Channel 0:", round(voltage, 2), "V")
    if(voltage < 2.3):
     # see if tripped for more than 2 seconds
     if(is_tripped):
       tripped_time_sec = tripped_time_sec + time.time()
       if(tripped_time_sec > 2):
         light_on()
     else:
       tripped_time_sec = 0 
       is_tripped = True 
    # else not tripped (not dropped below 2.3v
    else:
     tripped_time_sec = 0
     is_tripped = False
     light_off()
    time.sleep(0.2)

except KeyboardInterrupt:
  GPIO.cleanup()

