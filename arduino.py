import serial
import time

def send_light(color):
    # Replace 'COMx' with the actual serial port of your Arduino (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
    arduino_port = '/dev/ttyACM0'  

    # Establish serial connection
    ser = serial.Serial(arduino_port, 9600, timeout=1)
    # Allow time for the Arduino to reset after establishing the connection
   
    ser.write(color.encode)

    ser.close()
