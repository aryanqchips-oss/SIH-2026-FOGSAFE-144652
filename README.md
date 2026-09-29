# SIH-2026-FOGSAFE-144652
SIH-FOG-NAVIGATION-System
# ECHO — Intelligent Mining Safety Rover

> **ECHO** is an AI-enabled mining safety rover designed for real-time object detection, sensor monitoring, hazard awareness, and connected vehicle/command-center operation.

---

## 🚀 Overview

ECHO combines **AI-based object detection, onboard sensors, edge computing, communication, and real-time dashboards** into a unified mining-safety system.

The system is designed to help detect potential hazards, process information locally, and provide safety information to operators and the Command Center.

### Core Pipeline


Sensors / Camera
       ↓
Data Processing
       ↓
YOLO11s Object Detection
       ↓
Sensor Information
       ↓
Risk / Hazard Assessment
       ↓
Vehicle Dashboard
       ↓
V2V Communication
       ↓
Command Center

🧠 Key Features
AI Object Detection using YOLO11s
Real-time Edge Processing
Sensor Data Integration
Vehicle Safety Dashboard
Command Center Dashboard
V2V Communication
Real-time Hazard Alerts
Fleet / Rover Monitoring
Low-visibility perception using thermal imaging
Distance and motion awareness using sensors

🤖 AI Model

ECHO uses a trained YOLO11s object-detection model.

AI Pipeline
Input Image
     ↓
Image Pre-processing
     ↓
YOLO11s
     ↓
Object Detection
     ↓
Class + Bounding Box + Confidence
     ↓
Safety / Dashboard Output
Model Development
Dataset
   ↓
Data Preparation
   ↓
YOLO Training
   ↓
Validation
   ↓
Testing
   ↓
Best Model
   ↓
Edge Deployment

The training notebook is located in:

ai_model/Train_YOLO_Models.ipynb
⚡ Edge Processing

ECHO is designed for local processing so that AI inference and sensor processing can be performed close to the vehicle/rover.

Edge Hardware

Raspberry Pi 4B

Used for:

Real-time object detection
Sensor processing
Sensor fusion
Risk assessment
Dashboard communication

📡 Sensors & Hardware
Thermal Camera

Used for object perception in:

Fog
Dust
Low-light conditions
Radar

Used for:

Target detection
Distance estimation
Relative velocity
GPS / GNSS

Used for:

Position
Speed
Heading
IMU

Used for:

Vehicle motion
Acceleration
Orientation
Ultrasonic Sensor

Used for:

Short-range obstacle detection
Proximity measurement

🚛 Vehicle / Rover Dashboard

The dashboard provides real-time information such as:

AI detections
Object class
Detection confidence
Sensor information
Vehicle status
Hazard alerts
Communication status

Project location:

truck_dashboard/

Main application:

truck_dashboard/app.py

🏢 Command Center

The Command Center provides centralized monitoring of connected vehicles/rovers.

It can display:

Vehicle status
Vehicle location
Detected hazards
Alerts
Communication status
Fleet awareness

Dashboard:

command_centre_dashboard/fogsafe.html

📶 V2V Communication
ECHO supports the concept of sharing safety information between connected vehicles.
A vehicle can transmit information such as:

Position
Velocity
Heading
Sensor Data
Detected Hazard
Alert Status
Communication Flow
        ECHO / VEHICLE     ->    Sensor + AI Data  ->       V2V Communication ->  Nearby Vehicle ->  Command Center

This allows one vehicle detecting a potential hazard to share relevant information with nearby connected vehicles and the Command Center.

🛡️ Safety Pipeline
Object Detection
Object Association
Distance + Velcity
Risk Assessment
SAFE / WARNING / CRITICAL
Driver Alert
V2V / Command Center
Time-to-Collision
TTC = D / Vrel

Where:

D = distance to detected object
Vrel = relative closing velocity
Stopping Distance
ds = vtr + v² / 2a

Where:

v = vehicle speed
tr = reaction time
a = deceleration
🛠️ Technology Stack
AI / Computer Vision
Python
YOLO11s
Ultralytics
PyTorch
OpenCV
Google Colab
Edge Computing
Raspberry Pi 4B
Python
NCNN
Hardware
Thermal Camera
Radar
GPS / GNSS
IMU
Ultrasonic Sensor
ESP32
Communication
Wi-Fi
UDP / TCP
V2V Communication
Command Center Communication
Dashboard
Python
Flask
HTML
CSS
JavaScript


🧪 Testing

The project includes testing of:

AI object detection
Test images
Recorded videos
Dashboard operation
Sensor integration
Communication
Edge inference

Test media is stored under:

echo/

🎯 Project Objective
The objective of ECHO is to build an intelligent mining-safety platform that can:

Sense the surrounding environment
Detect objects using AI
Process sensor information locally
Assess potential hazards
Alert the vehicle operator
Communicate safety information to nearby vehicles
Monitor connected vehicles through a Command Center

🔮 Future Scope
Improved multi-sensor fusion
Advanced collision prediction
Multi-rover coordination
Improved V2V communication
Autonomous navigation
More optimized edge AI inference
Expanded object-detection classes
Mine-wide connected safety network

🌐 System Vision
ECHO ->AI SENSING -> SENSORS->EDGE PROCESSING->RISK AWARENESS->V2V ->COMMAND CENTER->CONNECTED MINE
       
👥 Project
ECHO — Intelligent Mining Safety Rover

AI + Sensors + Edge Computing + V2V + Command Center

Sense → Detect → Assess → Alert → Connect
