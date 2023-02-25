import tkinter as tk
import RPi.GPIO as GPIO
import time as time
import picamera
import os
import base64
import requests
#HOST = '192.168.219.148'
#PORT = 9009

pic_number = 1
root = tk.Tk()
camera = picamera.PiCamera()
response = '';
CAPTURETIMING = 37 # arduino 8
ABNORMAL = 33 # arduino 9
NORMAL = 31 # arduino 10
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(CAPTURETIMING, GPIO.IN)
GPIO.setup(ABNORMAL, GPIO.OUT)
GPIO.setup(NORMAL, GPIO.OUT)

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)

        
def checkCapture():
    
    while True:
        if GPIO.input(CAPTURETIMING):
            print(GPIO.input(CAPTURETIMING))
            getfile()
            break
        else:
            time.sleep(1)
            

def getfile():
    global pic_number
    pic_number += 1
    print(pic_number)
    
    camera.capture('/home/pi/Desktop/image' + str(pic_number) + '.jpg')
    with open('/home/pi/Desktop/image' + str(pic_number) + '.jpg', 'rb') as img:
        base64_string = base64.b64encode(img.read())
        base64_string = base64_string.decode('utf-8')
        url = "http://49.166.144.238:1323/image"

        response = requests.post(url, json={"image": base64_string, "name": "image" + str(pic_number) + ".jpg"})
        if response.text == "normal":
            GPIO.output(NORMAL, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(NORMAL, GPIO.LOW)
            print("normal")
        else:
            GPIO.output(ABNORMAL, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(ABNORMAL, GPIO.LOW)        
            print("ABNORMAL OR ERROR : " + response.text)
            
        checkCapture()
        
        
def camera_st():
    camera.resolution=(640, 480)
    camera.start_preview(fullscreen=False, window=(200, 200, 640, 480))
    checkCapture()

def camera_sp():
    camera.stop_preview()
    
def close_win():
    root.destroy
    camera.stop_preview()
    camera.close()
    GPIO.cleanup()
    quit()
    
def camera_ct():
    try:
        getfile()
    finally:
        print('End')

        
# Make a file-like object out of the connection
def cameraman():
    root.title("camera TEST")
    root.geometry("250x200+1000+50")

    frame = tk.Frame(root)
    frame.pack(pady = 0, padx = 0)

    button1 = tk.Button(frame, text = "start", width=20, padx=20, pady=10, command=camera_st)
    button1.grid(row = 0, column = 0, padx = 1, pady = 3)

    button2 = tk.Button(frame, text = "stop", width=20, padx=20, pady=10, command=camera_sp)
    button2.grid(row = 1, column = 0, padx = 1, pady = 3)

    button3 = tk.Button(frame, text = "capture", width=20, padx=20, pady=10, command=camera_ct)
    button3.grid(row = 2, column = 0, padx = 1, pady = 3)

    # button4 = tk.Button(frame, text = "runserver", width=20, padx=20, pady=10, command=runServer)
    # button4.grid(row = 3, column = 0, padx = 1, pady = 3)
        
    root.protocol("WM_DELETE_WINDOW", close_win)
    root.mainloop()

    
cameraman()
