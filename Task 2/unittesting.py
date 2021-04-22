import unittest
import udp
import random
import string
import struct

class TestUDP(unittest.TestCase):
    def test_calculate_checksum(self):
        #THE DATA IN THE WELCOME PACKET NEEDED TO TEST THE CALCULATE CHECKSUM
        source_port = 10
        dest_port = 42
        payload = 'Welcome to IoT UDP Server'
        
        #THE VALUE OUR CALCULATE CHECKSUM FUNCTION SHOULD RESULT IN
        checksum = 15307

        self.assertEqual(udp.calculate_checksum(source_port, dest_port, bytearray(payload.encode())), checksum)

if __name__ == '__main__':
    unittest.main()
