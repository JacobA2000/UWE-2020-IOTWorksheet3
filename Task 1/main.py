import asyncio

import websockets
import json

import time
import base64
import struct

async def recv_packet(websocket):
    packet = await websocket.recv()

    print(f"Base64: {packet}")
    return  base64.b64decode(packet)

async def recv_decode_packet(websocket):
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

async def main():
    uri = "ws://localhost:5612"

    async with websockets.connect(uri) as websocket:
        
        await recv_decode_packet(websocket)

asyncio.get_event_loop().run_until_complete(main())