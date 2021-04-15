# **iot-worksheet-3**

## **Task 1**
For Task 1, I had to recieve and decode the welcome message's UDP packet.

We do this by slicing the returned packet and converting into the correct data type. In our case mostly int but also utf-8 for the string payload.
```py
packet = await recv_packet(websocket)
print(f"UDP: {packet}")   

source_port = int.from_bytes(packet[0:2], "little")
print(f"Source Port: {source_port}")

dest_port = int.from_bytes(packet[2:4], "little")
print(f"Dest Port: {dest_port}")

length = int.from_bytes(packet[4:6], "little")
print(f"Length: {length}")

checksum = int.from_bytes(packet[6:8], "little")
print(f"Checksum: {checksum}")

payload = packet[8:(length+8)].decode("utf-8")
print(f"Payload: {payload}")
```

After decoding each slice is printed out and we recieve the following output:
```bash
(iot_env) jacob2.allen@live.uwe.ac.uk@CSImageBuild:~/projects/iot-worksheet-3$ /home/jacob2.allen/projects/iot_env/bin/python "/home/jacob2.allen/projects/iot-worksheet-3/Task 1/main.py"
Base64: b'CgAqACEAyztXZWxjb21lIHRvIElvVCBVRFAgU2VydmVy'
UDP: b'\n\x00*\x00!\x00\xcb;Welcome to IoT UDP Server'
Source Port: 10
Dest Port: 42
Length: 33
Checksum: 15307
Payload: Welcome to IoT UDP Server
```
***
## **Task 2**
Task 2 required me to calculate the sent packet's checksum, this checksum should be equal to the checksum sent in the packet. This is done to ensure we've recieved a valid packet.

Todo this I implemented the calculate_checksum function:
```py
def calculate_checksum(source_port: int, dest_port: int, length: int, payload: bytearray):
    """Calculates the checksum of the udp packet."""

    checksum = 0

    #Converting the passed info into byte form
    source = source_port.to_bytes(2, byteorder="little")
    dest = dest_port.to_bytes(2, byteorder="little")
    size = length.to_bytes(2, byteorder="little")
    checksum_bytes = checksum.to_bytes(2, byteorder="little")
    #Creating the byte array for the checksum
    checksum_packet = source + dest + size + checksum_bytes + payload

    if len(checksum_packet) % 2 != 0:
        checksum_packet += struct.pack("!B", 0)

    for i in range(0, length, 2):
        w = (checksum_packet[i] << 8) + (checksum_packet[i+1])
        checksum += w

    #Performing ones compliment
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF

    print(f"Calculated Checksum: {checksum}")
    return checksum
```
Running this calculation on the welcome message packet resulted proved that the packet recieved was valid and that the checksum calculation is correct:
```bash
(iot_env) jacob2.allen@live.uwe.ac.uk@CSImageBuild:~/projects/iot-worksheet-3$ /home/jacob2.allen/projects/iot_env/bin/python3 "/home/jacob2.allen/projects/iot-worksheet-3/Task 2/main.py"
Base64: b'CgAqACEAyztXZWxjb21lIHRvIElvVCBVRFAgU2VydmVy'
UDP: b'\n\x00*\x00!\x00\xcb;Welcome to IoT UDP Server'
Source Port: 10
Dest Port: 42
Length: 33
Checksum: 15307
Payload: Welcome to IoT UDP Server
Calculated Checksum: 15307
```