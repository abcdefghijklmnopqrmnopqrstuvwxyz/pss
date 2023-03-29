import numpy as np
import requests
import cv2
import serial.tools.list_ports
import serial


def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "Arduino Uno" in desc:
            return port
    return None


arduino = find_arduino()
rate = 9600
ser = serial.Serial(arduino, rate, timeout=1)
url = 'http://192.168.0.110/capture'

while True:
    response = requests.get(url)
    if response.status_code == 200:
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        plate_cascade = cv2.CascadeClassifier('eu_cascade.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(plates) > 0:
            print("1")
            data = 1
        else:
            print("0")
            data = 0
        ser.write(bytes([data]))
    else:
        print("Image not loaded")

ser.close()
