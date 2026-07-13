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

## Hardware pinout

All GPIO numbers below use **BCM numbering** (`GPIO.setmode(GPIO.BCM)`). The
physical-pin column refers to the Raspberry Pi's 40-pin header.

| Device / signal | BCM GPIO | Physical header pin | Direction / notes |
|---|---:|---:|---|
| DHT22 data | GPIO 4 | 7 | Input; temperature and humidity sensor |
| LED DO1 | GPIO 17 | 11 | Output |
| LED DO2 | GPIO 27 | 13 | Output |
| LED DO3 | GPIO 22 | 15 | Output |
| LED DO4 | GPIO 23 | 16 | Output |
| Relay / door lock control | GPIO 18 | 12 | Output; HIGH = unlock, LOW = lock |
| MG90S door-servo signal | GPIO 19 | 35 | PWM output |
| LED DO5 | GPIO 16 | 36 | Output |
| LED DO6 | GPIO 20 | 38 | Output |
| LED DO7 | GPIO 12 | 32 | Output |
| LED DO8 | GPIO 21 | 40 | Output |
| Flame-sensor digital output | GPIO 24 | 18 | Input; active LOW with internal pull-up |
| Smoke-sensor digital output | GPIO 26 | 37 | Input; active LOW with internal pull-up |
| Buzzer control | GPIO 25 | 22 | Output |
| L298N motor enable (ENA) | GPIO 13 | 33 | PWM output at 1 kHz |
| L298N motor direction (IN1) | GPIO 5 | 29 | Output |
| L298N motor direction (IN2) | GPIO 6 | 31 | Output |
| LCD I²C SDA | GPIO 2 / SDA1 | 3 | I²C bus 1 |
| LCD I²C SCL | GPIO 3 / SCL1 | 5 | I²C bus 1 |

The LCD is configured as a 16×2 PCF8574 I²C display at address `0x27` on I²C
bus 1. Connect each module's power and ground pins to a suitable supply and a
common Raspberry Pi ground. Do not power motors or a servo directly from a Pi
GPIO or 5 V rail unless the power budget has been verified; use an appropriate
external supply and retain the common ground.

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
Voice command activation ("open")
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
