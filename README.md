# **iot-worksheet-3**

This worksheet required me to experiment with the udp packet protocol, by recieving, verifying (checking the checksum is valid) and sending udp packets. 

Unfortunately, due to the asynchronous nature of the tasks, there was not much I could write unit tests for. However, I have implemented a test to ensure my calculate checksum is valid as this is not an async function.

## **Task 1**
For Task 1, I had to recieve and decode the welcome message's UDP packet.

We do this by slicing the returned packet and converting into the correct data type. In our case mostly int but also utf-8 for the string payload.
```py
packet = await recv_packet(websocket)
source_port = int.from_bytes(packet[0:2], "little")
dest_port = int.from_bytes(packet[2:4], "little")
length = int.from_bytes(packet[4:6], "little")
checksum = int.from_bytes(packet[6:8], "little")
payload = packet[8:(length+8)].decode("utf-8")
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
def calculate_checksum(source_port: int, dest_port: int, payload: bytearray) -> int:
    """Calculates the checksum of the udp packet."""

    checksum = 0
    #Calculate the length of the packet, by adding 8 (the length of the header) plus the length of the payload.
    length = 8 + len(payload)

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
I also wrote the following unit test to verify that this function worked as expected:
```py
def test_calculate_checksum(self):
        #THE DATA IN THE WELCOME PACKET NEEDED TO TEST THE CALCULATE CHECKSUM
        source_port = 10
        dest_port = 42
        payload = 'Welcome to IoT UDP Server'
        
        #THE VALUE OUR CALCULATE CHECKSUM FUNCTION SHOULD RESULT IN
        checksum = 15307

        self.assertEqual(udp.calculate_checksum(source_port, dest_port, bytearray(payload.encode())), checksum)
```
Running the unit test resulted in a pass:
```bash
(iot_env) jacob2.allen@live.uwe.ac.uk@CSImageBuild:~/projects/iot-worksheet-3$ /home/jacob2.allen/projects/iot_env/bin/python3 "/home/jacob2.allen/projects/iot-worksheet-3/Task 2/unittesting.py"
.
----------------------------------------------------------------------
Ran 1 test in 0.030s

OK
```
***
## **Task 3**
Task 3 required me to send a udp packet to the socket, this would then return a packet containing the current UTC time.

Todo this I implmented the send_packet function which takes in the desired header and payload data then converts it to byte form encodes it to base64 and then sends the packet to the socket.
```py
async def send_packet(websocket, source_port: int, dest_port: int, payload) -> None:
    """Sends a packet to the server using the given header and payload data."""
    #Convert the given data into bytes.
    source = source_port.to_bytes(2, "little")
    dest = dest_port.to_bytes(2, "little")
    length = 8 + len(payload)
    size = length.to_bytes(2, "little")
    checksum_bytes = calculate_checksum(source_port, dest_port, payload).to_bytes(2, "little")
    
    #Create the udp packet bytes.
    packet = source + dest + size + checksum_bytes + payload
    #Encode the packet into base64.
    packet = base64.b64encode(packet)

    #Send the packet.
    await websocket.send(packet)
```

After running this code we can see it works as we get a packet returned every second containing the current time. As can be seen below:

<img src="assets/Task 3 Demo.gif">