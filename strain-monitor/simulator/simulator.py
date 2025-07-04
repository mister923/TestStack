import socket
import struct
import math
import time

UDP_IP = "127.0.0.1"  # Use local loopback unless sending to another host
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t0 = time.time()

while True:
    t = time.time() - t0
    timestamp_ms = int(t * 1000)

    # Generate 10 synthetic readings (sine waves with different phase/frequency)
    readings = []
    for i in range(10):
        freq = 0.1 + i * 0.05  # Slightly different frequency per channel
        phase = i * 0.3
        val = 2048 + int(1024 * math.sin(2 * math.pi * freq * t + phase))
        val = max(0, min(val, 4095))  # Clamp to 12-bit ADC range
        readings.append(val)

    # Pack into binary: 8 bytes timestamp + 10 × 2-byte uint16
    packet = struct.pack("<Q10H", timestamp_ms, *readings)

    sock.sendto(packet, (UDP_IP, UDP_PORT))
    time.sleep(0.1)  # 10Hz
