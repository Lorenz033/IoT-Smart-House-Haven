# 📘 Smart Haven IoT System (Raspberry Pi + MQTT + MVC)

## 🧠 Overview

Smart Haven is an IoT-based automation system built using:

- Raspberry Pi 5
- MQTT communication
- Node-RED Dashboard
- Face Recognition (OpenCV + face_recognition)
- Voice Recognition (Vosk)
- LCD Display (I2C)
- GPIO Relay Control
- DC Motor Control (L298N + PWM)
- MVC software architecture

The system supports:
- Smart door access (face + voice authentication)
- Relay control (lock/unlock)
- DC motor speed control via Node-RED slider
- Scenario-based automation (Welcome / Leaving mode)

---

Node-RED Dashboard
↓
MQTT Broker
↓
App Controller (Brain)
↓
────────────────────────
| Scenario Logic |
| Services Layer |
| Model (State) |
| View (LCD Display) |
────────────────────────
↓
Raspberry Pi GPIO / PWM


⚙️ Features
🔐 Smart Door System
Face recognition authentication
Voice command activation (“automatic”)
Automatic unlock/lock via relay
📺 LCD Feedback
System status display
Welcome / Goodbye messages
Real-time feedback
📡 MQTT Communication
Topic	Function
WSA2025/DI1	Scenario trigger button
WSA2025/RELAY01	Manual relay control
WSA2025/MOTOR01	DC motor speed control

DC motor buttons should publish to `WSA2025/MOTOR01`:
- `50` for 50 percent speed
- `75` for 75 percent speed
- `100` for 100 percent speed
- `OFF` to stop the motor
