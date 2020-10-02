import struct
import paho.mqtt.client as mqtt  # import the client

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

broker_address = "127.0.0.1"
client = mqtt.Client("Master")  # create new instance
client.connect(broker_address)  # connect to broker
#    Width
# A ------- B
# |         |
# |         | Height
# |         |
# D ------- C
Height, Width = 16.5, 22  # Inches
# TODO: Add Calibration Phase
while True:
    x, y = input("Enter X Y\n")
    if x > Width and y > Height:
        continue
    new_lengths = [distance(x, y, x2, y2) for x2, y2 in [
        (0, 0), (Width, 0), (Width, Height), (0, Height)]]
    for name, length in zip(["A", "B", "C", "D"], new_lengths):
        client.publish(name, struct.pack('f', length))  # publish
        # float x = *(float *)&float_temp;
