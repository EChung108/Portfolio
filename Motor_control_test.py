## import necessary libraries
import time
import RPi.GPIO as GPIO

## configure GPIO pin setup 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

## set GPIO pin numbers for each motor
scalpel_pins = [2, 3, 4, 17]
scissor_pins = [27, 22, 18, 23]
dispense1_pins = [10, 9, 11, 24]
dispense2_pins = [5, 25, 8, 7]
Tray_pins1 = [6, 13, 19] ## 6 =SLP, 13 = step, 19 = DIR
Tray_pins2 = [12, 16, 20] ## 12 =SLP, 16 = step, 20 = DIR

## set up how much stepper motor turns (512 for one full turn)
quarter_turn = 128
turn_ratio = 4 * quarter_turn
scalpels = 10
scissors = 10
count_scalpels = 0
count_scissors = 0
tools_out = []

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

    ## put motor into sleep mode to reduce power consumption
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

    ## put motor into sleep mode to reduce power consumption
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

##initialise sample inventory system


##main function
def main():
    global scalpels
    global scissors
    global count_scalpels
    global count_scissors
    tool_request = ''
    past_tool_request = ''
    current_tray_posn = 'down'
    
    ## loop until told not to
    while True:

        ## display menu and wait for user input
        print('Please select tool: \n1: scalpel\n2: scissors\nor type dispense to dispense tools')
        tool_request = input()

        ## if 1 is put in, dispnese scalpel using scalpels motor, add '1' to tools_out and remove one from stock of scalpels
        if tool_request =='1':
            scalpels += -1
            
            if scalpels > 0:
                tools_out.extend('1')
                
                print('Dispensing scalpel')
                time.sleep(0.5)

                if current_tray_posn == 'up':
                    dispense_tool(scalpel_pins)
                    past_tool_request = '1'
                else: 
                    raise_tray(Tray_pins1, Tray_pins2)
                    time.sleep(0.1)
                    dispense_tool(scalpel_pins)
                    past_tool_request = '1'
   
                current_tray_posn = 'up'

            ## if no scalpels left in stock, print message and do not dispense scalpel
            else:
                scalpels = 0
                print('Sorry, there are no more scalpels left, please restock')
                time.sleep(0.5)

        ## if 2 is put in, dispense scissots using scissors motor, add '2' to tools_out an remove one from stock of scissors
        elif tool_request == '2':
            scissors += -1
            
            if scissors > 0:
                tools_out.extend('2')
                
                print('dispensing scissors')
                time.sleep(0.5)

                if current_tray_posn == 'up':
                    dispense_tool(scissor_pins)
                    past_tool_request = '2'
                else: 
                    raise_tray(Tray_pins1, Tray_pins2)
                    time.sleep(0.1)
                    dispense_tool(scissor_pins)
                    past_tool_request = '2'

                current_tray_posn = 'up'
            
            ## if no scissors left in stock, print message and do not dispense scissors
            else:
                scissors = 0
                print('Sorry, there are no more scissors left, please restock')
                time.sleep(0.5)

        ## if 3 or 'dispense' is put in, dispense tools using dispener motors 1 and 2, list requested tools  
        elif tool_request == 'dispense' or tool_request == '3':
            print('Dispensing your request tools')
    
            for items in tools_out:
                for tools in items:
                    if tools == '1':
                        count_scalpels += 1
                    elif tools == '2':
                        count_scissors += 1
                
            print(tools_out)
            time.sleep(0.5)
            print(f'you requested:\n{count_scalpels} x scalpels\n{count_scissors} x scissors')
            time.sleep(0.5)
        
            
            if current_tray_posn == 'up':
                lower_tray(Tray_pins1, Tray_pins2)
                time.sleep(0.1)
                dispense_tray(dispense1_pins, dispense2_pins)
                time.sleep(3)
                retract_tray(dispense1_pins, dispense2_pins)
            else:
                dispense_tray(dispense1_pins, dispense2_pins)
                time.sleep(3)
                retract_tray(dispense1_pins, dispense2_pins)
            current_tray_posn = 'down'

        ## if exit typed in then exit program
        elif tool_request =='exit' or tool_request == 'e':
            if current_tray_posn == 'up':
                lower_tray(Tray_pins1, Tray_pins2)
                print('exiting program')
            else:
                print('exiting program')
            GPIO.cleanup()
            exit()
        
        elif tool_request == '4':
            if current_tray_posn == 'down':
                raise_tray(Tray_pins1, Tray_pins2)
            else:
                print('Tray is already raised')
            current_tray_posn = 'up'
        
        elif tool_request == '5':
            if current_tray_posn == 'up':
                lower_tray(Tray_pins1, Tray_pins2)
            else:
                print('Tray is already lowered')
            current_tray_posn = 'down'

        ## if any other input is entered, print message
        else:
            print('Sorry, you have not picked a valid option, please try again')
            time.sleep(0.5)

if __name__ == '__main__':
    main()