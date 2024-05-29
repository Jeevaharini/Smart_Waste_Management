
import RPi.GPIO as GPIO
import time
import sys
from urllib.request import urlopen
import json
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
TRIG = 38
ECHO = 36
TRIG_PIN_1 = 22
ECHO_PIN_1 = 15
TRIG_PIN_2 = 16
ECHO_PIN_2 = 13
TRIG_PIN_3 = 18
ECHO_PIN_3 = 12
soil_sensor_pin = 23
servo_pin = 24
servo_pin2 = 37
GPIO.setup(TRIG_PIN_1, GPIO.OUT)
GPIO.setup(ECHO_PIN_1, GPIO.IN)
GPIO.setup(TRIG_PIN_2, GPIO.OUT)
GPIO.setup(ECHO_PIN_2, GPIO.IN)
GPIO.setup(TRIG_PIN_3, GPIO.OUT)
GPIO.setup(ECHO_PIN_3, GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(soil_sensor_pin, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)
servo = GPIO.PWM(servo_pin,50)
servo2 = GPIO.PWM(servo_pin2,50)
myAPI = 'B3I5VHAF7OT6XAIT'
baseURL = 'https://api.thingspeak.com/update?api_key=B3I5VHAF7OT6XAIT'
servo.start(0)
servo2.start(0)
GPIO.output(TRIG, False)
def read_soil_moisture(pin):
    if GPIO.input(pin):
        return False  # No water detected
    else:
        return True   # Water detected
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    servo.ChangeDutyCycle(0)

def set_angle2(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin2, True)
    servo2.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin2, False)
    servo2.ChangeDutyCycle(0)
   
def control_servo1(water_detected):
    if water_detected:
        set_angle(90)
        time.sleep(1)
        set_angle(45)
        time.sleep(1)
        set_angle(90)
        time.sleep(1)
    else:
        set_angle(90)
        time.sleep(1)
        set_angle(135)
        time.sleep(1)
        set_angle(90)
        time.sleep(1)
       
def control_servo2(predicted):
    if predicted=="Organic":
        set_angle2(90)
        time.sleep(1)
        set_angle2(0)
        time.sleep(1)
    elif predicted=="Recycle":
        set_angle2(270)
        time.sleep(1)
        set_angle2(0)
        time.sleep(1)
       
       
       
while True:
   
    print ('Calibrating.....')
    time.sleep(0.2)
    print ('Place the object......')
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance-0.5 , 2)
    print ("distance:",distance,"cm")
    time.sleep(2)
    if distance < 9 :
       
         # Adjust duration of rotation as needed

        # Main loop
        try:
           
            water_detected = read_soil_moisture(soil_sensor_pin)  # Read soil moisture sensor
            if water_detected:
                control_servo1(water_detected)
                print('Wet Waste!')
                        #GPIO.output(channel1, GPIO.LOW)
                try:
                    #GPIO.output(channel1, GPIO.LOW)
                    GPIO.output(TRIG_PIN_1, False)
                    print ('Calibrating.....')
                    time.sleep(0.2)
                    print ('Place the object......')
                    GPIO.output(TRIG_PIN_1, True)
                    time.sleep(0.00001)
                    GPIO.output(TRIG_PIN_1, False)

                    while GPIO.input(ECHO_PIN_1)==0:
                        pulse_start = time.time()
                    while GPIO.input(ECHO_PIN_1)==1:
                        pulse_end = time.time()
                    pulse_duration = pulse_end - pulse_start
                    distance1 = pulse_duration * 17150
                    distance1 = round(distance1-0.5 , 2)
                    print ("wet:",distance1,"cm")
                    if isinstance(distance1, float):
                         # Sending the data to thingspeak
                        conn = urlopen(baseURL + '&field1=%s' % (distance1))
                        print (conn.read())
                         # Closing the connection
                        conn.close()
                    else:
                        print ('Error')
                        sleep(2)

                except Exception as e:
                    print(str(e))
                    break
                time.sleep(2)    

            else:
               
                control_servo1(water_detected)
               
                print('Dry Waste!')
                predicted=input("Enter Predicted :")
                control_servo2(predicted)
                if predicted == "Organic":
                    try:
                        print('Organic Waste!')
                        #GPIO.output(channel1, GPIO.LOW)
                        GPIO.output(TRIG_PIN_2, False)
                        print ('Calibrating.....')
                        time.sleep(0.2)
                        print ('Place the object......')
                        GPIO.output(TRIG_PIN_2, True)
                        time.sleep(0.00001)
                        GPIO.output(TRIG_PIN_2, False)

                        while GPIO.input(ECHO_PIN_2)==0:
                            pulse_start1 = time.time()
                        while GPIO.input(ECHO_PIN_2)==1:
                            pulse_end1 = time.time()
                        pulse_duration1 = pulse_end1 - pulse_start1
                        distance2 = pulse_duration1 * 17150
                        distance2 = round(distance2-0.5 , 2)
                        print ("Organic:",distance2,"cm")
                        if isinstance(distance2, float):
                             # Sending the data to thingspeak
                            conn = urlopen(baseURL + '&field2=%s' % (distance2))
                            print (conn.read())
                             # Closing the connection
                            conn.close()
                        else:
                            print ('Error')
                            sleep(2)

                    except Exception as e:
                        print(str(e))
                        break
                    time.sleep(2)
                else:
                    try:
                        print('Recyclable Waste!')
                    #GPIO.output(channel1, GPIO.LOW)
                        GPIO.output(TRIG_PIN_3, False)
                        print ('Calibrating.....')
                        time.sleep(0.2)
                        print ('Place the object......')
                        GPIO.output(TRIG_PIN_3, True)
                        time.sleep(0.00001)
                        GPIO.output(TRIG_PIN_3, False)

                        while GPIO.input(ECHO_PIN_3)==0:
                            pulse_start = time.time()
                        while GPIO.input(ECHO_PIN_3)==1:
                            pulse_end = time.time()
                        pulse_duration = pulse_end - pulse_start
                        distance3 = pulse_duration * 17150
                        distance3 = round(distance3-0.5 , 2)
                        print ("Recycle:",distance3,"cm")
                        if isinstance(distance3, float):
                             # Sending the data to thingspeak
                            conn = urlopen(baseURL + '&field3=%s' % (distance3))
                            print (conn.read())
                             # Closing the connection
                            conn.close()
                        else:
                            print ('Error')
                            sleep(2)

                    except Exception as e:
                        print(str(e))
                        break
                    time.sleep(2)
             #  Control servo motor based on soil moisture level

        except KeyboardInterrupt:
            # Clean up GPIO
            servo.stop()
            GPIO.cleanup()
