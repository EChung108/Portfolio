##import relevent libraries
from ast import Num
import RPi.GPIO as GPIO
import  pygame
import time as t
from time import *
from pygame.locals import *
import cv2
from turtle import shape
import numpy as np
from _XiaoRGEEK_SERVO_ import XR_Servo
from hcsr04sensor import sensor
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
angle4 = 90
angle6 = 95
angle7 = 0

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
    angle1+=2
    Servo.XiaoRGEEK_SetServoAngle(1, angle1)
    return angle1, prev_angle1

## DEFINE Servo1 down (angle decrease)
def ServoONE_down():
    global angle1
    prev_angle1 = angle1
    angle1+=-2
    Servo.XiaoRGEEK_SetServoAngle(1, angle1)
    return angle1, prev_angle1


## Define servo2 up (angle increase)
def ServoTWO_up():
    global angle2
    prev_angle2 = angle2
    angle2+=2
    Servo.XiaoRGEEK_SetServoAngle(2, angle2)
    return angle2, prev_angle2

## define servo2 down (angle decrease)
def ServoTWO_down():
    global angle2
    prev_angle2 = angle2
    angle2+=-2
    Servo.XiaoRGEEK_SetServoAngle(2, angle2)
    return angle2, prev_angle2

## define servo3 rotate cw (angle increase)
def ServoTHREE_cw():
    global angle3 
    angle3+=2
    Servo.XiaoRGEEK_SetServoAngle(3, angle3)

## define servo3 reotate ccw (angle decrease)
def ServoTHREE_ccw():
    global angle3
    angle3+=-2
    Servo.XiaoRGEEK_SetServoAngle(3, angle3)

## define servo4 grip (angle increase)
def ServoFOUR_grip():
    global angle4  
    angle4+=2
    Servo.XiaoRGEEK_SetServoAngle(4, angle4)

## define servo4 ungrip (angle decrease)
def ServoFOUR_ungrip():
    global angle4
    angle4 +=-2
    Servo.XiaoRGEEK_SetServoAngle(4, angle4)

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
        angle6 = 95
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

    rad1 = m.radians(angle1)
    rad2 = m.radians(angle2)

    X1 = round(-9.5*m.cos(rad1 + m.radians(34)), 2)
    X2 = round(14.5*m.cos(rad2 + m.radians(18) - m.radians(34) - rad1 ), 2) 

    Y1 = 11.5 + round(9.5*m.sin(rad1 + m.radians(34)), 2)
    Y2 =  + round(14.5*m.sin(rad2 + m.radians(18)), 2) 

    print('length of arm 1', X1, 'length of arm 2', X2)
    

    Y_height = -6 + round(14.5 * m.sin(-rad2 + m.radians(90) + (rad1 + m.radians(34))) + 9.5 * m.sin(rad1 + m.radians(34)), 2)

    if PWMduty >=5 & PWMduty < 30:
        allowed_X_length = round((X1 + X2 + 15), 2)
    elif PWMduty >= 30 & PWMduty < 60:
        allowed_X_length = round((X1 + X2 + 25), 2)
    elif PWMduty >= 60 & PWMduty < 90:
        allowed_X_length = round((X1 + X2 + 33), 2)
    elif PWMduty >= 90 & PWMduty < 100:
        allowed_X_length = round((X1 + X2 + 35), 2)
    return allowed_X_length, Y_height


#assign values to PWMduty, PWM_L, PWM_R from PWM_initialise function
PWMduty,PWM_L,PWM_R = PWM_initialise()

run = True
prev_angle1 = 0
prev_angle2 = 0
distance_from_wall = distance()
allowed_X_distance, allowed_Y_distance = arm_length(PWMduty)
# main loop to read keyboard inputs
while run:
    
    if angle1 != prev_angle1 or angle2 != prev_angle2:
    

        allowed_X_distance, allowed_Y_distance = arm_length(PWMduty) 

        print(" allowed distance from the wall: ", allowed_X_distance, " allowed distance from the floor: ", allowed_Y_distance)

        prev_angle1 = angle1
        prev_angle2 = angle2
    else:

# fetches event queue ad reads queue
        for event in pygame.event.get():
            distance_from_wall = distance()
            if event.type ==pygame.QUIT:
                run = False

#If a key is pressed down then ...
            if event.type == pygame.KEYDOWN:

                

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
                    GPIO.cleanup()
                    exit()
               
#If all keys up, then stop
            elif event.type == pygame.KEYUP:
                Stop() 







