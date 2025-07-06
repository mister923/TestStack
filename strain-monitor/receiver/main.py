# Main receiver service for strain monitoring and GPS
import socket
import struct
import os
import requests
import sys
import signal

def signal_handler(signum, frame):
    print(f"Received signal {signum}, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

print("Starting receiver service...")

UDP_PORT = int(os.getenv("UDP_PORT", 12345))
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
INFLUX_ORG = os.getenv("INFLUX_ORG")

print(f"UDP_PORT: {UDP_PORT}")
print(f"INFLUX_URL: {INFLUX_URL}")
print(f"INFLUX_TOKEN: {INFLUX_TOKEN}")
print(f"INFLUX_BUCKET: {INFLUX_BUCKET}")
print(f"INFLUX_ORG: {INFLUX_ORG}")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    print(f"Successfully bound to UDP port {UDP_PORT}")
except Exception as e:
    print(f"Error binding to UDP port: {e}")
    sys.exit(1)

def send_to_influx(lines):
    url = f"{INFLUX_URL}/api/v2/write?org={INFLUX_ORG}&bucket={INFLUX_BUCKET}&precision=ms"
    headers = {
        "Authorization": f"Token {INFLUX_TOKEN}",
        "Content-Type": "text/plain"
    }
    try:
        resp = requests.post(url, data="\n".join(lines), headers=headers)
        if resp.status_code >= 300:
            print(f"Influx error: {resp.status_code} - {resp.text}")
        else:
            print("Influx:", resp.status_code)
    except Exception as e:
        print("Influx error:", e)

print(f"Listening on UDP port {UDP_PORT}")

while True:
    try:
        data, _ = sock.recvfrom(1024)

        if len(data) == 28:
            try:
                # Attempt strain gauge unpack: 8-byte timestamp + 10×uint16
                timestamp, = struct.unpack_from("<Q", data, 0)
                readings = struct.unpack_from("<10H", data, 8)
                lines = [
                    f"strain_gauge,id={i} value={v} {timestamp}"
                    for i, v in enumerate(readings)
                ]
                print(f"[Strain] {timestamp}: {readings}")
                send_to_influx(lines)

            except Exception:
                try:
                    # Attempt GPS unpack: 8-byte timestamp + 2×double + float
                    timestamp, = struct.unpack_from("<Q", data, 0)
                    lat, lon = struct.unpack_from("<dd", data, 8)
                    alt, = struct.unpack_from("<f", data, 24)
                    lines = [
                        f"gps location_lat={lat},location_lon={lon},altitude={alt} {timestamp}"
                    ]
                    print(f"[GPS] {timestamp}: lat={lat}, lon={lon}, alt={alt}")
                    send_to_influx(lines)

                except Exception as e:
                    print("Unrecognized packet format:", e)

        else:
            print(f"Ignored packet (unexpected length {len(data)} bytes)")

    except KeyboardInterrupt:
        print("Receiver interrupted.")
        break
    except Exception as e:
        print("Receiver error:", e)
