##########################
# Chi-Kin Chung          #
# 2160550                #
# IDP team 11            #   
# Meng ESEE 4            #
# Motor control to drive #
# stepper motors to push #
# out requested tool     #
# onto tray, raise and   #
# lower tray, and        #
# calibrate linear screw #
##########################

## import necessary libraries
import time
import RPi.GPIO as GPIO
from ArrDis import *

## configure GPIO pin setup 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

## set GPIO pin numbers for each motor
scalpel_pins = [2, 3, 4, 17]
scissor_pins = [27, 22, 18, 23]
dispense1_pins = [10, 9, 11, 24]
dispense2_pins = [5, 25, 8, 7]
Tray_pins1 = [6, 13, 19] ## 6 =SLP, 13 = step, 19 = DIR
Tray_pins2 = [16, 20, 21] ## 12 =SLP, 16 = step, 20 = DIR

## set up how much stepper motor turns (512 for one full turn)
quarter_turn = 128
turn_ratio = 4 * quarter_turn

##initialise inventory system tracking
scalpels = 0
scissors = 0
count_scalpels = 0
count_scissors = 0
tools_out = []
current_tray_posn ='lowered'

## set all GPIO pins used for motors as output and initial state as low
for pin in scalpel_pins:
  GPIO.setup(pin, GPIO.OUT, initial= GPIO.LOW)

for pin in scissor_pins:
  GPIO.setup(pin, GPIO.OUT, initial= GPIO.LOW)

for pin in dispense1_pins:
  GPIO.setup(pin, GPIO.OUT, initial= GPIO.LOW)

for pin in dispense2_pins:
  GPIO.setup(pin, GPIO.OUT, initial= GPIO.LOW)

for pin in Tray_pins1:
  GPIO.setup(pin, GPIO.OUT, initial= GPIO.LOW)

for pin in Tray_pins2:
  GPIO.setup(pin, GPIO.OUT, initial= GPIO.LOW)


## define function to turn stepper motor to push requested tool out
def dispense_tool(stepper_pins):
    global turn_ratio
    global scalpel_pins
    global scissor_pins
    global scalpels
    global scissors
    ## define sequence of coils to spin motor
    forward_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
    ]

    ## defines how long motor turns for
    for i in range(turn_ratio):

        ## cycles through all configurations in sequence
        for halfstep in range(8):

            ## applies configurations to all pins
            for pin in range(4):

                GPIO.output(stepper_pins[pin], forward_seq[halfstep][pin])
                time.sleep(0.0001)

    ## set all coils to inactive to stop power draw
    GPIO.output(stepper_pins, [0, 0, 0, 0])
    if stepper_pins == scalpel_pins:
        scalpels += -1
        dispup(scissors, scalpels)
    elif stepper_pins == scissor_pins:
        scissors+= -1
        dispup(scissors, scalpels)

## define function to raise tray using linear screw actuators
def raise_tray(Tray_pins1, Tray_pins2):
    global turn_ratio

    GPIO.output(Tray_pins1[0], True)
    GPIO.output(Tray_pins1[2], True)

    GPIO.output(Tray_pins2[0], True)
    GPIO.output(Tray_pins2[2], True)
    for i in range(3300):
        GPIO.output(Tray_pins1[1], True)
        GPIO.output(Tray_pins2[1], True)
        time.sleep(0.0003)
        GPIO.output(Tray_pins1[1], False)
        GPIO.output(Tray_pins2[1], False)
        time.sleep(0.0003)
    
    ## set all coils to inactive to stop power draw
    GPIO.output(Tray_pins1, [0, 0, 0])
    GPIO.output(Tray_pins2, [0, 0, 0])

## define function to lower tray using linear screw actuators
def lower_tray(Tray_pins1, Tray_pins2):
    global turn_ratio

    GPIO.output(Tray_pins1[0], True)
    GPIO.output(Tray_pins1[2], False)

    GPIO.output(Tray_pins2[0], True)
    GPIO.output(Tray_pins2[2], False)
    for i in range(3300):
        GPIO.output(Tray_pins1[1], True)
        GPIO.output(Tray_pins2[1], True)
        time.sleep(0.0003)
        GPIO.output(Tray_pins1[1], False)
        GPIO.output(Tray_pins2[1], False)
        time.sleep(0.0003)

    ## set all coils to inactive to stop power draw
    GPIO.output(Tray_pins1, [0, 0, 0])
    GPIO.output(Tray_pins2, [0, 0, 0])

## define function to dispense tray using stepper motors
def dispense_tray(dispense1_pins, dispense2_pins):
    global turn_ratio

    ## define sequence of coils to spin motor
    forwards_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
    ]

    ## defines how long motor turns for
    for i in range(turn_ratio):

        ## cycles through all configurations in sequence
        for halfstep in range(8):

            ## applies configurations to all pins
            for pin in range(4):

                GPIO.output(dispense1_pins[pin], forwards_seq[halfstep][pin])
                GPIO.output(dispense2_pins[pin], forwards_seq[halfstep][pin])
                time.sleep(0.0001)

    ## set all coils to inactive to stop power draw
    GPIO.output(dispense1_pins, [0, 0, 0, 0])
    GPIO.output(dispense2_pins, [0, 0, 0, 0])

## define function to dispense tray using stepper motors
def retract_tray(dispense1_pins, dispense2_pins):
    global turn_ratio

    ## define sequence of coils to spin motor
    backwards_seq = [
    [1,0,0,0],
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0]
    ]

    ## defines how long motor turns for
    for i in range(turn_ratio):

        ## cycles through all configurations in sequence
        for halfstep in range(8):

            ## applies configurations to all pins
            for pin in range(4):

                GPIO.output(dispense1_pins[pin], backwards_seq[halfstep][pin])
                GPIO.output(dispense2_pins[pin], backwards_seq[halfstep][pin])
                time.sleep(0.0001)

    ## set all coils to inactive to stop power draw       
    GPIO.output(dispense1_pins, [0, 0, 0, 0])
    GPIO.output(dispense2_pins, [0, 0, 0, 0])



