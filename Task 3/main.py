import asyncio
import websockets
import base64
import struct

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

async def send_packet(websocket, source_port: int, dest_port: int, payload):
    source_port = source_port.to_bytes(2, "little")
    dest_port = dest_port.to_bytes(2, "little")

    payload = bytes(str(payload), "utf-8")

    packet = source_port + dest_port + payload

    await websocket.send(packet)

async def recv_packet(websocket):
    """Recvieves the udp packet."""
    packet = await websocket.recv()

    print(f"Base64: {packet}")
    return  base64.b64decode(packet)

async def decode_packet(websocket):
    """Decodes the recvied packet"""
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

    #await send_packet(websocket, source_port, dest_port, payload)
    #CALCULATE THE CHECKSUM
    calculated_checksum = calculate_checksum(source_port,dest_port,length,bytearray(payload.encode()))
    
    if calculated_checksum != checksum:
        print("Checksums do not match INVALID PACKET!")

async def main():
    uri = "ws://localhost:5612"

    async with websockets.connect(uri) as websocket:
        
        await send_packet(websocket, 0, 542, b"1111")

        await decode_packet(websocket)

asyncio.get_event_loop().run_until_complete(main())