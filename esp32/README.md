# ESP32 GPS Project

This project uses PlatformIO to build and upload GPS data collection firmware to an ESP32 device.

## Hardware Requirements

- ESP32 development board (T-Beam recommended for GPS)
- GPS module (typically connected to UART1)
- WiFi connection

## Pin Configuration

- GPS RX: Pin 34
- GPS TX: Pin 12
- GPS UART: UART1

## Setup Instructions

### 1. Install PlatformIO

If you haven't installed PlatformIO yet:

```bash
# Install PlatformIO Core
pip install platformio

# Or install PlatformIO IDE extension in VS Code
```

### 2. Configure WiFi Settings

Edit `src/main.cpp` and update the WiFi credentials:

```cpp
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
```

### 3. Configure UDP Destination

Update the UDP destination in `src/main.cpp`:

```cpp
const char* udpAddress = "192.168.1.100"; // IP of your receiver
const int udpPort = 12345;
```

### 4. Build and Upload

```bash
# Build the project
pio run

# Upload to ESP32
pio run --target upload

# Monitor serial output
pio device monitor
```

## Data Format

The ESP32 sends 28-byte UDP packets containing:
- Timestamp (8 bytes, uint64_t)
- Latitude (8 bytes, double)
- Longitude (8 bytes, double)
- Altitude (4 bytes, float)

## Troubleshooting

- Ensure your ESP32 is connected via USB
- Check that the correct COM port is selected
- Verify WiFi credentials are correct
- Make sure the UDP receiver is running and accessible

## Dependencies

- TinyGPSPlus: GPS parsing library
- WiFi: Built-in ESP32 WiFi library
- WiFiUdp: Built-in ESP32 UDP library 