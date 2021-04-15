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