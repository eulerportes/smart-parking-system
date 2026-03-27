# 🚗 Smart Parking LPR Backend

Event-driven parking control system with License Plate Recognition (LPR) simulation, real-time processing, and secure administrative control.

---

## 📌 Overview

This project is a backend system designed to simulate and manage a parking lot using License Plate Recognition (LPR) events.

It processes incoming vehicle data via HTTP, applies business rules (such as capacity limits and duplicate filtering), and controls access decisions (entry/exit) with a modular and extensible architecture.

The system is designed to be **hardware-independent**, allowing easy integration with real LPR cameras (Intelbras, Hikvision, Dahua, etc.) and IoT devices (e.g., relay controllers like Shelly).

---

## ⚙️ Features

* 🚀 REST API built with Flask
* 🔄 Event-driven processing (`/lpr`)
* 🧠 Payload normalization (multi-vendor ready)
* ⏱️ Anti-duplicate logic (TTL-based)
* 🎯 Minimum confidence filtering
* 🚗 Entry / Exit control logic
* 🅿️ Parking capacity management
* 📂 Persistent state (JSON-based)
* 📋 Real-time status endpoints
* ⭐ Whitelist (external JSON file)
* 🔁 Live whitelist reload (no restart required)
* 🔐 Admin endpoint protected with API Key
* 🚧 Simulated gate control (ready for real hardware integration)

---

## 🏗️ Architecture

```text
Client / LPR Camera / Simulator
              │
              ▼
        Flask API (/lpr)
              │
              ▼
     Payload Normalization
              │
              ▼
     Parking Service Logic
   (TTL, capacity, whitelist)
              │
              ├── Save state (JSON)
              ├── Logging
              └── Gate Control (simulated)
```

---

## 📁 Project Structure

```text
smart-parking-system/
│
├── app/
│   ├── main.py
│   ├── services/
│   │   ├── parking_service.py
│   │   └── gate_service.py
│   └── utils/
│       └── payload_utils.py
│
├── logs/
│   ├── events.log
│   ├── parking_state.json
│   └── whitelist.json
│
├── simulator.py
├── app.py
└── requirements.txt
```

---

## 🔌 API Endpoints

### ▶️ POST `/lpr`

Receives LPR events.

#### Example request:

```json
{
  "plate": "ABC1D23",
  "confidence": 95,
  "direction": "in",
  "timestamp": "2026-03-26T10:00:00"
}
```

#### Example response:

```json
{
  "ok": true,
  "result": {
    "status": "entry",
    "plate": "ABC1D23",
    "inside_count": 1,
    "capacity": 10
  }
}
```

---

### 📊 GET `/status`

Returns system state.

```json
{
  "inside_count": 2,
  "capacity": 10,
  "available_spots": 8,
  "vehicles_inside": ["ABC1D23", "XYZ9K88"],
  "whitelist_count": 2
}
```

---

### 🚗 GET `/vehicles`

Returns current vehicles inside:

```json
{
  "vehicles_inside": ["ABC1D23", "XYZ9K88"]
}
```

---

### 🔄 POST `/admin/reload-whitelist`

Reloads whitelist file without restarting the server.

#### Required header:

```text
X-API-KEY: 123456
```

#### Response:

```json
{
  "ok": true,
  "whitelist_count": 4
}
```

---

## 📂 Whitelist Configuration

File:

```text
logs/whitelist.json
```

Example:

```json
[
  "ABC1D23",
  "VIP0001",
  "MENS123"
]
```

Rules:

* Whitelisted vehicles can enter even if parking is full
* Reload via `/admin/reload-whitelist`

---

## 🧪 Simulator

Run:

```bash
python simulator.py
```

Simulates LPR camera events with random plates.

---

## ▶️ Running the Project

### 1. Activate environment

```bash
venv\Scripts\activate
```

### 2. Run server

```bash
python app.py
```

### 3. Run simulator

```bash
python simulator.py
```

---

## 🔐 Security

Admin endpoints require API key:

```text
X-API-KEY: your-secret-key
```

---

## 🔌 Future Improvements

* Integration with real LPR cameras (Intelbras, Hikvision, etc.)
* Real relay control (Shelly / IoT devices)
* Authentication system (JWT)
* Database integration (PostgreSQL)
* Web dashboard (React / Vue)
* Multi-camera support

---

## 💼 Use Cases

* Parking automation systems
* Access control systems
* Smart city infrastructure
* IoT + backend integration projects
* Computer vision system integration

---

## 🛠️ Tech Stack

* Python 3
* Flask
* JSON (persistence)
* REST API
* Event-driven architecture

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Euler Campos Portes  
Electrical Engineer | Backend & IoT Integration  

Brazil  
🔗 LinkedIn: (add later if you want)

Developed as a backend engineering and IoT integration project.

---
