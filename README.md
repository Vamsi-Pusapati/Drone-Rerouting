# Drone Rerouting System

A comprehensive drone control and rerouting system that demonstrates GPS spoofing detection and mitigation capabilities. This project provides both backend drone control via MAVSDK and a web-based interface for real-time monitoring and control.

## 🚁 Project Overview

This system consists of two main components:
- **MAVSDK Communications**: Low-level drone control and telemetry reading
- **Web Interface**: Real-time web dashboard for drone monitoring and GPS spoofing attack simulation

## 📋 Features

### Core Capabilities
- **Real-time Drone Connection**: Connect to drones via UDP protocol
- **Telemetry Monitoring**: Live health status and position data
- **Flight Control**: Arm/disarm, takeoff, and landing capabilities
- **GPS Spoofing Simulation**: Demonstrate and detect GPS spoofing attacks
- **Web Dashboard**: Real-time monitoring via SocketIO

### MAVSDK Communications
- **Drone Connection Management**: Establish and maintain drone connections
- **Health Monitoring**: Check global position estimates and system health
- **Flight Mode Tracking**: Monitor current flight modes and states
- **Asynchronous Operations**: Non-blocking drone control operations

### Web Interface
- **Real-time Updates**: Live telemetry data via WebSocket connections
- **Interactive Controls**: Start/stop drone operations from web browser
- **Logging System**: Real-time log display for debugging and monitoring
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ System Architecture

```
Drone-Rerouting/
├── drone-mavsdk-communications/
│   ├── drone_connection.py       # Basic drone connection and control
│   ├── drone_arm_disarm.py       # Arm/disarm functionality
│   ├── drone_take_off_land.py    # Takeoff and landing operations
│   ├── drone_telemetry_reading.py # Telemetry data collection
│   ├── drone_position_ned.py     # Position tracking in NED coordinates
│   ├── drone_path_movement.py    # Path planning and movement
│   └── __init__.py
├── webserver/
│   ├── backend.py                # Flask backend with SocketIO
│   ├── drone_telemetry_reading.py # Web-specific telemetry handling
│   ├── templates/
│   │   └── index.html           # Web dashboard interface
│   └── backend.py               # Flask server with SocketIO
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- MAVSDK-Python
- Flask
- Flask-SocketIO
- Drone with MAVLink support (SITL or physical drone)

### Installation

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd Drone-Rerouting
   ```

2. **Install dependencies**
   ```bash
   pip install mavsdk flask flask-socketio
   ```

3. **Start the drone simulator (optional)**
   ```bash
   # For PX4 SITL
   make px4_sitl jmavsim
   ```

### Running the System

#### Option 1: MAVSDK Direct Control
```bash
cd drone-mavsdk-communications
python drone_connection.py
```

#### Option 2: Web Interface
```bash
cd webserver
python backend.py
```
Then open your browser to `http://localhost:5000`

## 📊 Usage Guide

### Basic Drone Operations
1. **Connect to Drone**: The system automatically connects via UDP on port 14550
2. **Check Health Status**: Verify global position estimate before flight
3. **Arm Motors**: Enable motor control
4. **Takeoff/Land**: Execute flight operations
5. **Monitor Telemetry**: Real-time position and status updates

### GPS Spoofing Detection
- **Baseline Establishment**: Record legitimate GPS coordinates
- **Anomaly Detection**: Compare real-time GPS with expected values
- **Alert System**: Web interface shows spoofing attempts in real-time
- **Mitigation**: Automatic return-to-home on spoofing detection

## 🔧 Configuration

### Drone Connection Settings
```python
# Default connection string
"udp://:14550"  # For SITL
"serial:///dev/ttyUSB0:57600"  # For physical drone via USB
"udp://192.168.1.100:14550"  # For network connection
```

### WebI have gathered enough information about the project structure and functionality. Here’s a draft for the README file:

```markdown
# Drone Rerouting System

## Overview
The Drone Rerouting System is designed to control a drone using MAVSDK and Flask. It allows users to start and stop drone operations through a web interface, providing real-time telemetry data and logs.

## Project Structure
```
.
├── drone-mavsdk-communications/
│   ├── __init__.py
│   ├── drone_arm_disarm.py
│   ├── drone_connection.py
│   ├── drone_path_movement.py
│   ├── drone_position_ned.py
│   ├── drone_take_off_land.py
│   ├── drone_telemetry_reading.py
├── webserver/
│   ├── backend.py
│   ├── drone_telemetry_reading.py
│   ├── templates/
│   │   └── index.html
└── README.md
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Drone-Rerouting
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the Flask web server:
   ```bash
   python webserver/backend.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Use the buttons on the web interface to start or stop the drone operations.

## Features
- **Start Drone**: Initiates the drone connection and begins telemetry reading.
- **Stop Drone**: Currently not implemented, but intended to stop the drone operations.
- **Real-time Logs**: Displays logs of the drone's actions and telemetry data.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
```

