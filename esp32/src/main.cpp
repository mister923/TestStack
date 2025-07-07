#include <WiFi.h>
#include <WiFiUdp.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>

// WiFi credentials
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// UDP destination
const char* udpAddress = "192.168.1.100"; // IP of your receiver
const int udpPort = 12345;

WiFiUDP udp;
TinyGPSPlus gps;

// Use T-Beam GPS UART (typically Serial1)
HardwareSerial GPSSerial(1); // UART1 on pins 34 (RX), 12 (TX)

const int GPS_RX = 34;
const int GPS_TX = 12;

void setup() {
  Serial.begin(115200);
  GPSSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected.");
}

void loop() {
  while (GPSSerial.available()) {
    gps.encode(GPSSerial.read());
  }

  if (gps.location.isUpdated()) {
    uint64_t timestamp = millis();
    double lat = gps.location.lat();
    double lon = gps.location.lng();
    float alt = gps.altitude.meters(); // Optional

    // Build 28-byte packet
    uint8_t packet[28];
    memcpy(packet, &timestamp, 8);         // 8 bytes
    memcpy(packet + 8, &lat, 8);           // 8 bytes
    memcpy(packet + 16, &lon, 8);          // 8 bytes
    memcpy(packet + 24, &alt, 4);          // 4 bytes

    udp.beginPacket(udpAddress, udpPort);
    udp.write(packet, sizeof(packet));
    udp.endPacket();

    Serial.printf("Sent GPS: lat=%.6f lon=%.6f alt=%.2f\n", lat, lon, alt);
  }

  delay(100); // ~10Hz sampling
}
