import struct
import paho.mqtt.client as mqtt  # import the client


def distance(x1, y1, z1, x2, y2, z2):
    return ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**.5


broker_address = "127.0.0.1"
client = mqtt.Client("Master")  # create new instance
client.connect(broker_address)  # connect to broker
#    Width
# A ------- B
# |         |
# |         | Length
# |         |
# D ------- C   # Height = Distance from the floor
Length, Width, Height = 41.91, 55.88, 30  # cm
# TODO: Add Calibration Phase
while True:
    client.loop_start()  # Start the Loop
    x, y, z = [int(i) for i in input("Enter X Y Z within bounds: \n").split()]
    if 0 > x > Width and 0 > y > Length and 0 > z > Height:
        print("Out of Bounds \n")
        continue
    new_lengths = [distance(x, y, z, x2, y2, z2) for x2, y2, z2 in [
        (0, 0, 0), (Width, 0, 0), (Width, Length, 0), (0, Length, 0)]]
    for name, length in zip(["A", "B", "C", "D"], new_lengths):
        client.publish(name, struct.pack('f', length))  # Publish
        print("{} Target: {} cm".format(name, length))
    client.loop_stop()  # Stop the Loop
