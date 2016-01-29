from __future__ import print_function
import time
from pololu_drv8835_rpi import motors, MAX_SPEED
import web
import RPi.GPIO as GPIO
import socket
import pygame
from datetime import datetime
import threading
    
UDP_IP = "192.168.0.2"
UDP_PORT = 5005

SPEED = 150;

diodesGpio = [20,21,17,26,16,18,27,24]
GPIO.setmode(GPIO.BCM)
 




class controler:
    def forward(self):
        try:
            motors.setSpeeds(0, 0)
            motors.motor1.setSpeed(SPEED)
            motors.motor2.setSpeed(SPEED)
        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "going forward"

    def back(self):
        self.lightDiodes(diodesGpio[0], diodesGpio[1])
        try:
            motors.setSpeeds(0, 0)
            motors.motor1.setSpeed(-SPEED)
            motors.motor2.setSpeed(-SPEED)
        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "going forward"
    
    def stop(self):
        try:
            self.turnOffDiodes(diodesGpio[0], diodesGpio[1])
            motors.setSpeeds(0, 0)
    

        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "stoped"
    
    def leftforward(self):
        try:
            motors.setSpeeds(0, 0)
            motors.motor1.setSpeed(SPEED/2)
            motors.motor2.setSpeed(SPEED)
    

        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "going forward"
    
    def rightforward(self):
        try:
            motors.setSpeeds(0, 0)
            motors.motor1.setSpeed(SPEED)
            motors.motor2.setSpeed(SPEED/2)
    

        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "going forward"

    def lightson(self):
        try:
            self.lightDiodes(diodesGpio[2],diodesGpio[3])
            self.lightDiodes(diodesGpio[4],diodesGpio[5])
            self.lightDiodes(diodesGpio[6],diodesGpio[7])
        except:
            GPIO.cleanup()
        return "going forward"
    def lightsoff(self):
        try:
            self.turnOffDiodes(diodesGpio[2],diodesGpio[3])
            self.turnOffDiodes(diodesGpio[4],diodesGpio[5])
            self.turnOffDiodes(diodesGpio[6],diodesGpio[7])    
        except:
            GPIO.cleanup()
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
        return "going forward"
    def left(self):
        try:
            motors.setSpeeds(0, 0)
            motors.motor1.setSpeed(-SPEED)
            motors.motor2.setSpeed(SPEED)
    

        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "going forward"
    
    def right(self):
        try:
            motors.setSpeeds(0, 0)
            motors.motor1.setSpeed(SPEED)
            motors.motor2.setSpeed(-SPEED)
    

        except:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
        return "going forward"
    
    def lightDiodes(self, gpio1, gpio2):
        GPIO.setmode(GPIO.BCM)
        self.turnOnGpio(gpio1)
        self.turnOnGpio(gpio2)

    def turnOffDiodes(self,gpio1, gpio2):
        GPIO.setmode(GPIO.BCM)
        self.turnOffGpio(gpio1)
        self.turnOffGpio(gpio2)

    def turnOnGpio(self,number):
        GPIO.setup(number, GPIO.OUT)
        GPIO.output(number, True)

    def turnOffGpio(self,number):
        GPIO.setup(number, GPIO.OUT)
        GPIO.output(number, False)
    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/iamrobot.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

lastRequest = datetime.now()



sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
c = controler()

def checkLastRequest():
    now = datetime.now()
    tdelta = now - lastRequest
    seconds = tdelta.total_seconds()
    if seconds>1:          
        c.stop()
        print("stop")
    threading.Timer(1,checkLastRequest).start()

checkLastRequest()
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if data!="":
        lastRequest = datetime.now()
    if data=="forward":
        c.forward()
    elif data=="stop":
        c.stop()
    elif data=="right":
        c.right()
    elif data=="left":
        c.left()
    elif data=="leftforward":
        c.leftforward()
    elif data=="rightforward":
        c.rightforward()
    elif data=="back":
        c.back()
    elif data=="lightsoff":
        c.lightsoff()
    elif data=="lightson":
        c.lightson()
    elif data=="play":
        c.play()
    
    print ("received message:",data)

    
