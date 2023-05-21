## keyboard control scheme: 
# w = forwards
# s = backwards
# a = turn left
# d = turn right
# up arrow = raise arm
# down arrow = lower arm
# e = riase wrist
# q = lower wrist
# left arrow = rotate wrist CCW
# right arrow = rotate wrist CW
# 1 = increase travel speed
# 0 = decrease travel speed

##import relevent libraries
from ast import Num
import RPi.GPIO as GPIO
import  pygame
import time as t
import paho.mqtt.client as mqtt
from time import *
from pygame.locals import *
import cv2
from turtle import shape
import numpy as np
from _XiaoRGEEK_SERVO_ import XR_Servo
from hcsr04sensor import sensor
import os

##setting up XiaoR Geek servo motor board
Servo = XR_Servo()

# initialise pygame and set GPIO pins
pygame.init()
GPIO.setmode(GPIO.BCM)

##open screen for pygame input
screen = pygame.display.set_mode((400, 300))
##define ports
ENA=13
ENB=20
rForw=19
rRev=16
lRev=21
lForw=26
trig = 17
echo = 4

#Turn off warning messeges
GPIO.setwarnings(False)

##initialize GPIO output pins
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(rForw, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(rRev, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lRev, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lForw, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

##Initialize servo angle values
angle1 = 56
angle2= 72
angle3 = 86
angle4 = 60
angle6 = 100
angle7 = 0
KData = 260
KData_prev = 300
FData = 250
FData_prev = 300
Flex = 10900
Flex_prev = 11300
Mag = 0
MagInit = 180
Twist = 0
Flop = 0
Flat = 0
loop = 0


##initialize servo arm state
Servo.XiaoRGEEK_SetServoAngle(1, angle1)
Servo.XiaoRGEEK_SetServoAngle(2, angle2)
Servo.XiaoRGEEK_SetServoAngle(3, angle3)
Servo.XiaoRGEEK_SetServoAngle(4, angle4)
##initalize camera servo state
Servo.XiaoRGEEK_SetServoAngle(6, angle6)
Servo.XiaoRGEEK_SetServoAngle(7, angle7)
## save servo positions
Servo.XiaoRGEEK_SaveServo()


#define PWM set up and start
def PWM_initialise():
    PWMduty = 50
    
    ## Specify PWM control port and frequency
    PWM_L=GPIO.PWM(ENA,1000)
    PWM_R=GPIO.PWM(ENB,1000)

    ## PWM start
    PWM_L.start(PWMduty)
    PWM_R.start(PWMduty)

    return PWMduty, PWM_L, PWM_R

##define function to move forward
def Move_forward():
   
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,True)
    GPIO.output(rRev,False)
    GPIO.output(lRev,False)
    GPIO.output(lForw,True)
 

## defined move backwards
def Move_backwards():
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,False)
    GPIO.output(rRev,True)
    GPIO.output(lRev,True)
    GPIO.output(lForw,False) 


##define slow spin left
def Slow_spin_left():
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,True)
    GPIO.output(rRev,False)
    GPIO.output(lRev,False)
    GPIO.output(lForw,False)

## define slow spin right
def Slow_spin_right():
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,False)
    GPIO.output(rRev,False)
    GPIO.output(lRev,False)
    GPIO.output(lForw,True)


## define quick spin left
def Quick_spin_left():
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,True)
    GPIO.output(rRev,False)
    GPIO.output(lRev,True)
    GPIO.output(lForw,False)
 

## quick spin right
def Quick_spin_right():
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,False)
    GPIO.output(rRev,True)
    GPIO.output(lRev,False)
    GPIO.output(lForw,True)


## define servo1 up (angle increase)
def ServoONE_up():
    global angle1 
    prev_angle1 = angle1
    ## angle 1 cannot be above 168 degrees
    if angle1 >= 168:
        angle1 = 168
    else:
        angle1+=2

    Servo.XiaoRGEEK_SetServoAngle(1, angle1)
    return angle1, prev_angle1

## DEFINE Servo1 down (angle decrease)
def ServoONE_down():
    global angle1
    prev_angle1 = angle1
    ## doesn't allow angle 1 below 56 degrees
    if angle1 <= 56:
        angle1 = 56
    else:
        angle1+=-2
    Servo.XiaoRGEEK_SetServoAngle(1, angle1)
    return angle1, prev_angle1


## Define servo2 up (angle increase)
def ServoTWO_up():
    global angle2
    prev_angle2 = angle2
    ## angle 2 cannot be above 146 degrees
    if angle2 >= 146:
        angle2 = 146
    else:
        angle2+=2
    Servo.XiaoRGEEK_SetServoAngle(2, angle2)
    return angle2, prev_angle2

## define servo2 down (angle decrease)
def ServoTWO_down():
    global angle2
    prev_angle2 = angle2
    ## angle 2 cannot be below 30 degrees
    if angle2 <= 30:
        angle2 = 30
    else:
        angle2+=-2
    Servo.XiaoRGEEK_SetServoAngle(2, angle2)
    return angle2, prev_angle2

## define servo3 rotate cw (angle increase)
def ServoTHREE_cw():
    global angle3 
    ## angle 3 cannot be above 180 degrees
    if angle3 >= 180:
        angle3 = 180
    else:
        angle3+=2
    Servo.XiaoRGEEK_SetServoAngle(3, angle3)

## define servo3 reotate ccw (angle decrease)
def ServoTHREE_ccw():
    global angle3
    ## angle 3 cannot be below 0 degrees
    if angle3 <= 0:
        angle3 = 0
    else:
        angle3+=-2

    Servo.XiaoRGEEK_SetServoAngle(3, angle3)

## define servo4 grip (angle increase)
def ServoFOUR_grip():
    global angle4  
    ## angle 4 cannot be above 110 degrees
    if angle4 >= 110:
        angle4 = 110
    else:
        angle4+=2
    Servo.XiaoRGEEK_SetServoAngle(4, angle4)

## define servo4 ungrip (angle decrease)
def ServoFOUR_ungrip():
    global angle4
    ## angle 4 cannot be below 46 degrees
    if angle4 <= 46:
        angle4 = 46
    else:
        angle4 +=-2
    Servo.XiaoRGEEK_SetServoAngle(4, angle4)

## defines servo reset function to set servos back to original start-up position
def servo_reset():
        global angle1
        global angle2
        global angle3
        global angle4
        global angle6
        global angle7
        angle1 = 56
        angle2= 72
        angle3 = 86
        angle4 = 90
        angle6 = 100
        angle7 = 0
        Servo.XiaoRGEEK_SetServoAngle(1, angle1)
        Servo.XiaoRGEEK_SetServoAngle(2, angle2)
        Servo.XiaoRGEEK_SetServoAngle(3, angle3)
        Servo.XiaoRGEEK_SetServoAngle(4, angle4)
        Servo.XiaoRGEEK_SetServoAngle(6, angle6)
        Servo.XiaoRGEEK_SetServoAngle(7, angle7)


##define stop function
def Stop():
    GPIO.output(ENA,True)
    GPIO.output(ENB,True)
    GPIO.output(rForw,False)
    GPIO.output(rRev,False)
    GPIO.output(lRev,False)
    GPIO.output(lForw,False) 

##define PWM duty cycle increase function
def PWMduty_up(PWMduty, PWM_L, PWM_R):
    if PWMduty <=95:
        PWMduty +=5
        PWM_L.ChangeDutyCycle(PWMduty)
        PWM_R.ChangeDutyCycle(PWMduty)
        print("Current Duty Cycle: ", PWMduty)
    return (PWMduty, PWM_L, PWM_R)
    
# define PWM duty cycle decrease function
def PWMduty_down(PWMduty, PWM_L, PWM_R):
    if PWMduty >=10:
        PWMduty +=-5
        PWM_L.ChangeDutyCycle(PWMduty)
        PWM_R.ChangeDutyCycle(PWMduty)
        print("Current Duty Cycle: ", PWMduty)
    return (PWMduty, PWM_L, PWM_R)

 #define opening of stored image, grayscaling, rotating and resizing same image   

def image():
    
        img = cv2.imread("Test_image.jpg")

        ##Display image
        cv2.imshow('image', img)
        sleep(0.5)

        

        imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        cv2.imshow ('Greyscaled image', imgGrey)
        sleep(0.5)

       

        rotate = cv2.rotate(img, cv2.ROTATE_180)
        cv2.imshow('rotated', rotate)
        sleep(0.5)

        

        h, w, c = img.shape
        newsize = (h/2, w/2)
        resize = cv2.resize(img, newsize)
        cv2.imshow('resized', resize)
        sleep(0.5)
        if cv2.waitKey(0): 
            cv2.destroyAllWindows()


#defines opening on on board camera and capturing still image
def camera():
        
# Open the default camera
    cap = cv2.VideoCapture(1)
    sleep(0.1)

    # Capture a frame
    while True:    
        ret, frame = cap.read()

    # Display the captured frame
        cv2.imshow('Frame', frame)

        if cv2.waitKey(0):
            cv2.imwrite('Test_image.jpg', frame)
            break      
        # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    cap = None

#defines using the onboard hcsr04 ultrasonic sensor to sense distance in front of robot
def distance():
    import time
    pulse_start = 0
    pulse_end = 0
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(trig, GPIO.LOW)

    while GPIO.input(echo) == 0:
        pulse_start = t.time()
    while GPIO.input(echo) == 1:
        pulse_end = t.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = round((pulse_duration *34300)/2 , 2)
    
    print('Distance from wall is:', distance)
    return distance

#defines function to calculate x and y extention of robot arm using servo angles 
def arm_length(PWMduty):
    import math as m
    rad1 = 0
    rad2 = 0
    X1 = 0
    X2 = 0
    Y1 = 0
    Y2 = 0

    global angle1
    global angle2
    #convert angle1 and angle2 angles from degrees to radians
    rad1 = m.radians(angle1)
    rad2 = m.radians(angle2)

    #using kinematics, calculate the horizontal distance from the base 
    #to the end of the link of each arm link relative to the x axis
    X1 = round(-9.5*m.cos(rad1 + m.radians(34)), 2)
    X2 = round(14.5*m.cos(rad2 + m.radians(18) - m.radians(34) - rad1 ), 2) 

    #print values to confirm and for calibration
    # print('length of arm 1', X1, 'length of arm 2', X2)
    
   #using kinematics, calculate the veritcal height of the end of each arm link
    Y_height = + round(14.5 * m.sin(-rad2 + m.radians(90) + (rad1 + m.radians(34))) + 9.5 * m.sin(-rad1 + m.radians(34)), 2)

    #calculating the allowable horizontal distance from the wall to allow for roughly 2cm clearance from wall
    #depending on spped as more time is needed to stop when going at faster speeds
    if PWMduty >=5 & PWMduty < 30:
        allowed_X_length = round((X1 + X2 + 15), 2)
    elif PWMduty >= 30 & PWMduty < 60:
        allowed_X_length = round((X1 + X2 + 25), 2)
    elif PWMduty >= 60 & PWMduty < 90:
        allowed_X_length = round((X1 + X2 + 33), 2)
    elif PWMduty >= 90 & PWMduty < 100:
        allowed_X_length = round((X1 + X2 + 35), 2)
    return allowed_X_length, Y_height

    return allowed_X_length, Y_height

#connects pi to data stream for knuckle potetiometer on glove
def Connect_KnuckleData(client1, userdata, flags, rc):

    ##prints connection code
    print('Connected with result code ', rc)

    ##subscribes client 1 to data stream labelled below
    client1.subscribe("MadamHoppityKnuckleData")

#connects pi to data stream for finger potetiometer on glove
def Connect_FingerData(client2, userdata, flags, rc):

    ##prints connection code
    print('Connected with result code ', rc)

    ##subscribes client 2 to data stream labelled below
    client2.subscribe("MadamHoppityFingerData")

#connects pi to data stream for strain gauge on glove
def Connect_FlexData(client3, userdata, flags, rc):

    ##prints connection code
    print("Connected with result code ", rc)

    ##subscribes client 3 to data stream labelled below
    client3.subscribe("MadamHoppityFlexData")  

#connects pi to data stream for magnetometer on glove
def Connect_MagData(client4, userdata, flags, rc): 

    ##prints code to show connection
    print('Connected with result code ', rc)

    ##subscribes client 4 to data stream labelled below
    client4.subscribe("MadamHoppityMagnetData")

#connects pi to data stream for accelerometer of wrist in CW+CCw plane on glove
def Connect_TwistData(client5, userdata, flags, rc): 

    ##prints code to show connection
    print('Connected with result code ', rc)

    ##subscribes client 5 to data stream labelled below
    client5.subscribe("MadamHoppityTwistData")

#connects pi to data stream for accelerometer of wrist in U+D plane on glove
def Connect_FlopData(client6, userdata, flags, rc): 

    ##prints code to show connection
    print('Connected with result code ', rc)

    ##subscribes client 6 to data stream labelled below
    client6.subscribe("MadamHoppityFlopData")

def Connect_FlatData(client7, userdata, flags, rc): 

    ##prints code to show connection
    print('Connected with result code ', rc)

    ##subscribes client 7 to data stream labelled below
    client7.subscribe("MadamHoppityFlatData")

#reads data from knuckle potentiometer
def KnuckleData(client1, userdata, msg):
    global KData
    KData = int(msg.payload)
    
#reads data from finger potentiometer
def FingerData(client2, userdata, msg):
    global FData
    FData = int(msg.payload)
    
#reads data from strain gauge
def FlexData(client3, userdata, msg):
    global Flex
    Flex = int(msg.payload)
    
#reads data from magnetometer 
def MagData(client4, userdata, msg):
    global Mag
    Mag = int(msg.payload)

#reads data from accelerometer in CW+CCW plane
def TwistData(client5, userdata, msg):
    global Twist
    Twist = int(msg.payload)

#reads data from accelerometer in U+D plane
def FlopData(client6, userdata, msg):
    global Flop
    Flop = int(msg.payload)

def FlatData(client7, userdata, msg):
    global Flat
    Flat = int(msg.payload)
    
#defines function to allow glove to control robot depending on data recieved from glove
def glove_control(wall_distance, x_distance, y_distance, PWMduty,  PWM_L, PWM_R):
  
    global KData
    global FData
    global Flex
    global Mag
    global MagInit
    global Twist
    global Flop

    ## determines compass direction depending on data from mag and calibration from pico
    if Mag >= 0 and Mag < 45:
        print('W')
    elif Mag >= 45 and Mag < 90:
        print('SW')
    elif Mag >= 90 and Mag < 135:
        print('S')
    elif Mag >= 135 and Mag < 180:
        print('SE')
    elif Mag >= 180 and Mag < 225:
        print('E')
    elif Mag >= 225 and Mag < 270:
        print('NE')
    elif Mag >= 270 and Mag < 315:
        print('N')
    elif Mag >= 315 and Mag < 360:
        print('NW')
    else:
        print('this isnt possible!')

    ## determine range at which glove needs to rotate to turn robot
    if Mag >= (200+30):
        Quick_spin_left()
    elif Mag <= (200-30):
        Quick_spin_right()
    else:
        Stop()

    #define ranges at which servo motor angles increase or decrease for each collected data from glove
    if KData >= 310 :
        if allowed_Y_distance > 2:
           ServoONE_up()
        else:
            None
    elif KData <= 280:
        ServoONE_down()
    else:
        None

    if FData >= 400:
        if allowed_Y_distance > 2:
            ServoTWO_down()
        else:
            None
    elif FData <= 300:
        ServoTWO_up()
    else:
        None

    if Twist >= 7:
        ServoTHREE_ccw()
    elif Twist <= -7:
        ServoTHREE_cw()
    else:
        None
    if Flex >= 40000:
        ServoFOUR_grip()
    elif Flex <= 39000:
        ServoFOUR_ungrip()
    else:
        None



#limits added to stop arm from folding fully backwards and going outside of servos allowable range
#servo1 range: 30 to 170 degrees
#servo1 allowed range: 56 to 168 degrees
#servo2 range: 0 to 140 degrees
#servo2 allowed range: 30 to 146 degrees
#servo3 range: 0 to 180 degrees
#servo3 allowed range: 0 to 180 degrees
#servo4 range: 44 to 120 degrees
#servo allowed range: 46 to 110 degrees

    ##move robot forwards if glove is dipped forwards otherwise don't move
    if Flop <= -5:
        if wall_distance >= x_distance:
                PWMduty = int(round((-(Flop+2)*6.25)+50, 0))
                PWM_L.ChangeDutyCycle(PWMduty)
                PWM_R.ChangeDutyCycle(PWMduty)
                Move_forward()
            
        else:
           Stop()
    ## move robot backwards if glove is dipped backwards, otherwise don't move
    elif Flop >= 5:
        PWMduty = int(round(((Flop-2)*6.25)+50, 0))
        PWM_L.ChangeDutyCycle(PWMduty)
        PWM_R.ChangeDutyCycle(PWMduty)
        Move_backwards()
    
    else:
        Stop()
    

        





#assign values to PWMduty, PWM_L, PWM_R from PWM_initialise function
PWMduty,PWM_L,PWM_R = PWM_initialise()

run = True

#initialise variables prev_angle1 and prev_angle2
prev_angle1 = 0
prev_angle2 = 0

#call the distance function to calculate the distance from the wall on start up
distance_from_wall = distance()

# make clients1-4 mqtt clients
client1 = mqtt.Client()
client2 = mqtt.Client()
client3 = mqtt.Client()
client4 = mqtt.Client()
client5 = mqtt.Client()
client6 = mqtt.Client()
client7 = mqtt.Client()

#connect clients to respecetd data streams
client1.on_connect = Connect_KnuckleData
client1.on_message = KnuckleData

client2.on_connect = Connect_FingerData
client2.on_message = FingerData

client3.on_connect = Connect_FlexData
client3.on_message = FlexData

client4.on_connect = Connect_MagData
client4.on_message = MagData

client5.on_connect = Connect_TwistData
client5.on_message = TwistData

client6.on_connect = Connect_FlopData
client6.on_message = FlopData

client7.on_connect = Connect_FlatData
client7.on_message = FlatData

# set the will messages, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client1.will_set('raspberry/status', b'{"status": "Off"}')
client2.will_set('raspberry/status', b'{"status": "Off"}')
client3.will_set('raspberry/staus', b'{"status": "Off"}')
client4.will_set('raspberry/status', b'{"status": "Off"}')
client5.will_set('raspberry/status', b'{"status": "Off"}')
client6.will_set('raspberry/status', b'{"status": "Off"}')
client7.will_set('raspberry/status', b'{"status": "Off"}')


# create connections, the three parameters are broker address, broker port number, and keep-alive time respectively
client1.connect("broker.hivemq.com", 1883, 60)
client2.connect("broker.hivemq.com", 1883, 60)
client3.connect("broker.hivemq.com", 1883, 60)
client4.connect("broker.hivemq.com", 1883, 60)
client5.connect("broker.hivemq.com", 1883, 60)
client6.connect("broker.hivemq.com", 1883, 60)
client7.connect("broker.hivemq.com", 1883, 60)


#starts the data fetch loop to read data stream from glove
client1.loop_start()
client2.loop_start()
client3.loop_start()
client4.loop_start()
client5.loop_start()
client6.loop_start()
client7.loop_start()

sleep(2)

while loop !=10:
    #prints the x, y and z axis acceleromter data
    print('x, y, z data:', Twist, Flop, Flat)
    loop += 1

sleep(2)
# main loop to read inputs
while run:
    ## calculate distance away from wall
    distance_from_wall = distance()
    ## calculate the length and height of arm of robot to work our allowable distances
    allowed_X_distance, allowed_Y_distance = arm_length(PWMduty) 
    ##use glove control function to allow robot to be controlled wirelessly using glove
    glove_control(distance_from_wall, allowed_X_distance, allowed_Y_distance, PWMduty, PWM_L, PWM_R)
    
    #used to detect if arm has moved so new arm length and height can be calculated
    if angle1 != prev_angle1 or angle2 != prev_angle2:
    

        allowed_X_distance, allowed_Y_distance = arm_length(PWMduty) 

        prev_angle1 = angle1
        prev_angle2 = angle2
    else:

# fetches event queue and reads queue
        for event in pygame.event.get():

            

            if event.type ==pygame.QUIT:
                run = False

#If a key is pressed down then ...
            if event.type == pygame.KEYDOWN:
                #calculate the distance from the wall any time a button is pressed down
                distance_from_wall = distance()

                if event.key == pygame.K_w: 

                    if distance_from_wall >= allowed_X_distance:
                        Move_forward()
                    else:
                        break
                    

                elif event.key == pygame.K_s:
                    Move_backwards()
                   

                elif event.key == pygame.K_a:
                    Quick_spin_left()
                

                elif event.key == pygame.K_d:
                    Quick_spin_right()

                elif event.key == pygame.K_p:
                    camera()

                elif event.key == pygame.K_DOWN:
                    #if robot arm is further than 2 cm from the wall then allow arm movement
                    #if robot arm is 2 cm or closer to wall, then don't allow arm extention 
                    if allowed_Y_distance > 2:
                        angle1, prev_angle1 = ServoONE_up()
                    else:
                        break

                elif event.key == pygame.K_e:
                        angle2, prev_angle2 = ServoTWO_up()
            
                elif event.key == pygame.K_RIGHT:
                    ServoTHREE_cw()

                elif event.key == pygame.K_g:
                    ServoFOUR_grip()

                elif event.key == pygame.K_UP:
                    angle1, prev_angle1 = ServoONE_down()

                elif event.key == pygame.K_q:
                    #if robot arm is further than 2 cm from the wall then allow arm movement
                    #if robot arm is 2 cm or closer to wall, then don't allow arm extention 
                    if allowed_Y_distance > 2:
                        angle2, prev_angle2 = ServoTWO_down()
                    else:
                        break

                elif event.key == pygame.K_LEFT:
                    ServoTHREE_ccw()

                elif event.key == pygame.K_f:
                    ServoFOUR_ungrip()

                elif event.key == pygame.K_1:
                    PWMduty,PWM_L,PWM_R = PWMduty_up(PWMduty, PWM_L, PWM_R)
                    sleep(0.1)

                elif event.key == pygame.K_0:
                    PWMduty,PWM_L,PWM_R = PWMduty_down(PWMduty, PWM_L, PWM_R)
                    sleep(0.1)

                elif event.key == pygame.K_i:
                    image()
                
                elif event.key == pygame.K_v:
                    cv2.destroyAllWindows()
                    cap = None
                elif event.key == pygame.K_r:
                    servo_reset()
                elif event.key == pygame.K_ESCAPE:
                    exit()
               
#If all keys up, then stop
            elif event.type == pygame.KEYUP:
                Stop() 

