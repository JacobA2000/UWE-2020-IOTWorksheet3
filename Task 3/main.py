import asyncio
import websockets
import base64
import struct
import time

def calculate_checksum(source_port: int, dest_port: int, payload: bytearray) -> int:
    """Calculates the checksum of the udp packet."""

    checksum = 0
    #Calculate length of payload by adding 8 (the length of the header), and the length of the payload together.
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

async def send_packet(websocket, source_port: int, dest_port: int, payload) -> None:
    source = source_port.to_bytes(2, "little")
    dest = dest_port.to_bytes(2, "little")
    length = 8 + len(payload)
    size = length.to_bytes(2, "little")
    checksum = calculate_checksum(source_port, dest_port, payload)
    checksum_bytes = checksum.to_bytes(2, "little")
    
    packet = source + dest + size + checksum_bytes + payload

    packet = base64.b64encode(packet)

    await websocket.send(packet)

async def recv_packet(websocket) -> bytes:
    """Recvieves the udp packet."""
    packet = await websocket.recv()

    print(f"Base64: {packet}")
    return base64.b64decode(packet)

async def decode_packet(websocket) -> None:
    """Decodes the recvied packet"""
    packet = await recv_packet(websocket)
    source_port = int.from_bytes(packet[0:2], "little")
    dest_port = int.from_bytes(packet[2:4], "little")
    length = int.from_bytes(packet[4:6], "little")
    checksum = int.from_bytes(packet[6:8], "little")
    payload = packet[8:(length+8)].decode("utf-8")
    
    #CALCULATE THE CHECKSUM
    calculated_checksum = calculate_checksum(source_port, dest_port, bytearray(payload.encode()))
    print(f"Calculated Checksum: {calculated_checksum}")

    if calculated_checksum != checksum:
        print("Checksums do not match INVALID PACKET!")
    else:
        print("-" * (24 + len(str(packet))))
        print(f"UDP:                    {packet}")
        print(f"Source Port:            {source_port}")
        print(f"Dest Port:              {dest_port}")
        print(f"Length:                 {length}")
        print(f"Checksum:               {checksum}")
        print(f"Payload:                {payload}")
        print(f"Calculated Checksum:    {calculated_checksum}")
        print("-" * (24 + len(str(packet))))

async def main() -> None:
    uri = "ws://localhost:5612"

    async with websockets.connect(uri) as websocket:
        
        await decode_packet(websocket)

        while True:
            await send_packet(websocket, 0, 542, b"1111")

            await decode_packet(websocket)

            time.sleep(1)

asyncio.get_event_loop().run_until_complete(main())