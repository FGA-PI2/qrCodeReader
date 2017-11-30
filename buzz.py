#!/usr/bin/python

import os
import time
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)


def erro():

  t_end = time.time() + 1
  while time.time() < t_end:
      GPIO.output(2,GPIO.HIGH)
      sleep(.2)
      GPIO.output(2,GPIO.LOW)
      sleep(.2)
      GPIO.output(2,GPIO.HIGH)
      sleep(.2)
      GPIO.output(2,GPIO.LOW)
      sleep(.2)

def lido():
   t_end = time.time() + 0.5
   while time.time() < t_end:
       GPIO.output(2,GPIO.HIGH)
       sleep(.5)
       GPIO.output(2,GPIO.LOW)



def sucesso():
   GPIO.output(2,GPIO.HIGH)
   sleep(.1)
   GPIO.output(2,GPIO.LOW)
   sleep(.1)
   GPIO.output(2,GPIO.HIGH)
   sleep(.1)
   GPIO.output(2,GPIO.LOW)


lido()

sleep(2)

erro()
sleep(2)
lido()
sleep(2)
sucesso()
