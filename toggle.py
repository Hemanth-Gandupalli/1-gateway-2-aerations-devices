import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(6, GPIO.HIGH)
    print("pin 6 is high")
    time.sleep(3)
    GPIO.output(6, GPIO.LOW)
    print("pin 6 is low")
    time.sleep(3)
    GPIO.output(23, GPIO.HIGH)
    print("pin 23 is high")
    time.sleep(3)
    GPIO.output(23, GPIO.LOW)
    print("pin 23 is low")
    time.sleep(3)
    GPIO.output(5, GPIO.HIGH)
    print("pin 5 is high")
    time.sleep(3)
    GPIO.output(5, GPIO.LOW)
    print("pin 5 is low")