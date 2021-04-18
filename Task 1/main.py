import asyncio
import websockets
import base64

async def recv_packet(websocket) -> bytes:
    """Recieves the udp packet."""
    packet = await websocket.recv()

    print(f"Base64: {packet}")
    #Decode the packet from base64 to bytes
    return base64.b64decode(packet)

async def decode_packet(websocket) -> None:
    """Decodes the recvied packet"""
    #Decode the data in the packet header and payload from bytes to they're relevant data types.
    packet = await recv_packet(websocket)
    source_port = int.from_bytes(packet[0:2], "little")
    dest_port = int.from_bytes(packet[2:4], "little")
    length = int.from_bytes(packet[4:6], "little")
    checksum = int.from_bytes(packet[6:8], "little")
    payload = packet[8:(length+8)].decode("utf-8")

    #Output the data
    print("-" * (24 + len(str(packet))))
    print(f"UDP:                    {packet}")
    print(f"Source Port:            {source_port}")
    print(f"Dest Port:              {dest_port}")
    print(f"Length:                 {length}")
    print(f"Checksum:               {checksum}")
    print(f"Payload:                {payload}")
    print("-" * (24 + len(str(packet))))

async def main() -> None:
    uri = "ws://localhost:5612"

    #Connect to the socket
    async with websockets.connect(uri) as websocket:
        
        await decode_packet(websocket)

asyncio.get_event_loop().run_until_complete(main())