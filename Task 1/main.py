import asyncio
import websockets
import base64

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

async def main():
    uri = "ws://localhost:5612"

    async with websockets.connect(uri) as websocket:
        
        await decode_packet(websocket)

asyncio.get_event_loop().run_until_complete(main())