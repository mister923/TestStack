# Strain Monitor

A real-time strain gauge monitoring system using Docker containers for data collection, storage, and visualization.

## Architecture

The system consists of four main components:

- **InfluxDB** - Time-series database for storing strain gauge measurements
- **Grafana** - Web-based visualization and dashboard platform
- **Receiver** - UDP listener that processes strain gauge data and writes to InfluxDB
- **Simulator** - Generates synthetic strain gauge data for testing

## Data Flow

```
Simulator → UDP → Receiver → InfluxDB → Grafana
```

## Prerequisites

- Docker and Docker Compose installed on your system
- Internet connection (for initial image downloads)

## Quick Start

### 1. Clone and Navigate

```bash
cd strain-monitor
```

### 2. Build and Start Services

```bash
# Build all services
docker-compose build

# Start all services in the background
docker-compose up -d
```

### 3. Access Grafana

- **URL**: http://localhost:3000
- **Username**: `admin`
- **Password**: `admin`

### 4. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see all four services (influxdb, grafana, receiver, simulator) in the "Up" state.

## Service Details

### InfluxDB
- **Port**: 8086
- **Purpose**: Stores time-series strain gauge data
- **Initial Setup**: Automatically configured with:
  - Organization: `myorg`
  - Bucket: `strain_bucket`
  - Admin Token: `mytoken`

### Grafana
- **Port**: 3000
- **Purpose**: Data visualization and dashboards
- **Auto-configuration**: 
  - InfluxDB datasource automatically configured
  - Basic strain dashboard available

### Receiver
- **UDP Port**: 12345
- **Purpose**: Listens for strain gauge data packets
- **Data Format**: Expects 28-byte UDP packets:
  - 8 bytes: timestamp (milliseconds)
  - 20 bytes: 10 strain gauge readings (2 bytes each)

### Simulator
- **Purpose**: Generates test strain gauge data
- **Frequency**: Sends data every second
- **Data**: Random values between 0-65535 for 10 strain gauges

## Data Format

The system expects UDP packets with the following structure:

```
[8 bytes timestamp][2 bytes gauge 0][2 bytes gauge 1]...[2 bytes gauge 9]
```

Total packet size: 28 bytes

## Stopping the System

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete all data)
docker-compose down -v
```

## Troubleshooting

### Service Won't Start

1. Check if ports are already in use:
   ```bash
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8086
   ```

2. View service logs:
   ```bash
   docker-compose logs [service-name]
   ```

### Receiver Not Receiving Data

1. Check if the receiver is listening:
   ```bash
   docker-compose logs receiver
   ```

2. Test UDP connectivity:
   ```bash
   # From another machine or container
   echo "test" | nc -u localhost 12345
   ```

### Grafana Dashboard Issues

1. Verify InfluxDB connection in Grafana:
   - Go to Configuration → Data Sources
   - Check if InfluxDB datasource is working

2. Check InfluxDB is running:
   ```bash
   docker-compose logs influxdb
   ```

## Development

### Adding Custom Dashboards

1. Create your dashboard in Grafana UI
2. Export as JSON
3. Place in `grafana/provisioning/dashboards/`
4. Update dashboard configuration if needed

### Modifying Data Processing

Edit `receiver/main.py` to change how incoming data is processed and stored.

### Custom Simulator

Edit `simulator/simulator.py` to generate different test data patterns.

## File Structure

```
strain-monitor/
├── docker-compose.yml          # Service orchestration
├── influxdb/
│   └── config/
│       └── influx-config.env   # InfluxDB configuration
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       │   └── strain_dashboard.json
│       └── datasources/
│           └── datasource.yaml
├── receiver/
│   ├── main.py                 # UDP listener and data processor
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile
└── simulator/
    ├── simulator.py            # Test data generator
    └── Dockerfile
```

## Environment Variables

Key environment variables used by the receiver:

- `UDP_PORT`: Port to listen for UDP packets (default: 12345)
- `INFLUX_URL`: InfluxDB API URL
- `INFLUX_TOKEN`: Authentication token
- `INFLUX_BUCKET`: Target bucket for data storage
- `INFLUX_ORG`: InfluxDB organization

## License

This project is provided as-is for educational and development purposes. 