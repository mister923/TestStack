import socket
import struct
import math
import time

UDP_IP = "receiver"  # Use Docker service name
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sending strain gauge data to {UDP_IP}:{UDP_PORT}")

t0 = time.time()

while True:
    timestamp_ms = int(time.time() * 1000)  # Use absolute timestamp

    # Generate 10 synthetic readings (sine waves with different phase/frequency)
    readings = []
    t = time.time() - t0  # Use relative time for sine wave calculation
    for i in range(10):
        freq = 0.1 + i * 0.05  # Slightly different frequency per channel
        phase = i * 0.3
        val = 2048 + int(1024 * math.sin(2 * math.pi * freq * t + phase))
        val = max(0, min(val, 4095))  # Clamp to 12-bit ADC range
        readings.append(val)

    # Pack into binary: 8 bytes timestamp + 10 × 2-byte uint16
    packet = struct.pack("<Q10H", timestamp_ms, *readings)

    sock.sendto(packet, (UDP_IP, UDP_PORT))
    print(f"Sent: timestamp={timestamp_ms}, readings={readings[:3]}...")
    time.sleep(0.1)  # 10Hz
