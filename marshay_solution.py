#!/usr/bin/env python3          
import signal
import sys
import RPi.GPIO as GPIO
import board
import time
import busio
from adafruit_ht16k33 import segments
ENTER_BUTTON_GPIO = 15
EXIT_BUTTON_GPIO = 18
LED_GPIO = 14
totalInLine = 0
lineStartTimes = []
lineExitTimes = []
timesInLine = []
estimatedWaitTime = 0
index = 0
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
def line_enter_callback(channel):
    if(GPIO.input(ENTER_BUTTON_GPIO)):
      lineStartTimes.append(time.time())
      GPIO.output(LED_GPIO, GPIO.HIGH)
      global totalInLine
      totalInLine = totalInLine + 1
      print(totalInLine)
      print(lineStartTimes)
    else:
      GPIO.output(LED_GPIO, GPIO.LOW)
def line_exit_callback(channel):
    if(GPIO.input(EXIT_BUTTON_GPIO)):
      lineExitTimes.append(time.time())
      GPIO.output(LED_GPIO, GPIO.HIGH)
      global totalInLine
      print(totalInLine)
      print(lineExitTimes)
      global index
      index = len(lineStartTimes) - totalInLine
      totalInLine = totalInLine - 1
      timesInLine.append(lineExitTimes[index] - lineStartTimes[index])
      global estimatedWaitTime
      if(totalInLine == 0):
        estimatedWaitTime = round(timesInLine[index]/60, 2)
      else:
        estimatedWaitTime = round(((timesInLine[index] * totalInLine)/60), 2)
      print("Index of Head of Line: " + str(index))
      print("estimated wait time:" + str(estimatedWaitTime))
      print(timesInLine)
    else:
      GPIO.output(LED_GPIO, GPIO.LOW)
#  This protects whatever code is placed beneath it from being executed when imported.  It is essentially defining this file as an application not a module.
if __name__ == '__main__':
    GPIO.setwarnings(False)  
#     GPIO.setmode(GPIO.BOARD)
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the LED segment class.
    # This creates a 7 segment 4 character display:
    display = segments.Seg7x4(i2c)
    # Clear the display.
    display.fill(0)
    GPIO.setup(ENTER_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(EXIT_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_GPIO, GPIO.OUT)   
    GPIO.add_event_detect(ENTER_BUTTON_GPIO, GPIO.BOTH, 
            callback=line_enter_callback)
    GPIO.add_event_detect(EXIT_BUTTON_GPIO, GPIO.BOTH, 
            callback=line_exit_callback)
#   The signal.SIGINT sends a keyboard event when 'control c' is pressed and signal_handler cleans up the GPIO assignments and closes the app.
    signal.signal(signal.SIGINT, signal_handler)
    display.print(str(totalInLine))
    while(True):
        if(totalInLine > 0):
            timeHeadSpendingInLine = round(((time.time() - lineStartTimes[index])/60), 2)
            if(len(timesInLine) == 0):
                estimatedWaitTime = timeHeadSpendingInLine * totalInLine
        time.sleep(2)
        display.fill(0)
        display.print(str(totalInLine))
        time.sleep(2)
        display.fill(0)
        display.print(str(estimatedWaitTime))
#   These two line pause the execution flow of the app so that the script stays open in the console and the callbacks stay active.
    signal.pause()
