import serial

ser = serial.Serial('COM4', 115200, timeout=None)


#TEST RAMP
for i in range(2**12):
    ser.write(bytes([i%256,i>>8]))
    print(ser.read(2))

#WRITE HIGH
# ser.write(bytes([15,255]))

#WRITE LOW
# ser.write(bytes([0,0]))
# print(ser.read(2))

# ser.write(bytes([255,255]))
# print(ser.read(2))

ser.close()