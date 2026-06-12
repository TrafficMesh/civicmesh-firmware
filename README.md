# CivicMesh Edge Node Firmware

Python firmware for Raspberry Pi CM4 edge nodes. Local AI inference, evidence capture, and uplink.

**Status:** Phase 1 (Implementation begins Q3 2026)

## Directory Structure

```
civicmesh-firmware/
├── firmware/
│   ├── main.py                  # Event loop orchestrator, system initialization
│   ├── camera_capture.py        # GStreamer H.264 video capture pipeline
│   ├── obd_interface.py         # OBD-II CAN bus reader (vehicle speed, diagnostics)
│   ├── gps_module.py            # u-blox NEO-M9N UART communication
│   ├── cellular_modem.py        # LTE modem upload manager and heartbeat
│   ├── edge_inference.py        # TensorFlow Lite model execution
│   ├── incident_builder.py      # Package detection → incident JSON
│   └── uploader.py              # Compress, encrypt, queue for upload
├── models/
│   ├── alpr.tflite              # Automatic License Plate Recognition (quantized)
│   ├── lane_detection.tflite    # Lane marking segmentation (quantized)
│   └── object_detection.tflite  # Vehicle, pedestrian, sign detection (quantized)
├── tests/
│   ├── unit/
│   │   ├── test_camera_capture.py     # GStreamer pipeline tests
│   │   ├── test_inference.py          # Model execution tests
│   │   └── test_uploader.py           # Compression and encryption tests
│   └── integration/
│       └── test_incident_pipeline.py  # Full capture → inference → upload
├── config/
│   ├── gpio_pinout.yaml         # RPi CM4 GPIO assignments (camera CSI, OBD UART, GPS UART, modem USB)
│   ├── inference_config.json    # Model paths, confidence thresholds, num_threads, GPU enable/disable
│   └── network_config.yaml      # Cellular APN, bands, fallback 2G, backend URL, buffer config
├── .github/workflows/
│   ├── ci.yml                   # Run tests, lint (pytest, flake8)
│   ├── firmware-build.yml       # Cross-compile ARM binaries for RPi CM4
│   └── model-quantization.yml   # (Phase 2) Optimize TFLite models for edge
├── requirements.txt             # TensorFlow Lite, gpiozero, pyserial, aiohttp, pytest
└── README.md                    # This file
```

## Firmware Modules

### Core Modules (Event-Driven Architecture)

#### **camera_capture.py** — Video Capture
- GStreamer pipeline: video source → H.264 encoder → frame buffer
- Resolution: 1440p @ 30fps
- Bitrate: 8-10 Mbps
- Output: Compressed H.264 clips to disk

#### **obd_interface.py** — Vehicle Interface
- CAN 500K parser (ISO 15765-2)
- Relevant PIDs:
  - 0x0D: Vehicle Speed (mph/kph)
  - 0x05: Engine Coolant Temperature
  - 0x10: Mass Air Flow
  - 0x31: Distance Traveled
- Returns: Dictionary of decoded values

#### **gps_module.py** — Location Tracking
- u-blox NEO-M9N via UART
- Outputs: Latitude, longitude, accuracy, timestamp
- Cold start: ~45s, Hot start: ~5s
- Update rate: 10Hz

#### **cellular_modem.py** — LTE Uplink
- Quectel EC25 modem management
- APN configuration (configurable per carrier)
- Fallback to 2G if LTE unavailable
- Heartbeat interval: 300s (configurable)

#### **edge_inference.py** — On-Device AI
- TensorFlow Lite interpreter
- Models:
  - **ALPR:** License plate recognition (tflite quantized)
  - **Lane Detection:** Marking segmentation
  - **Object Detection:** Vehicle, pedestrian, sign detection
- Confidence thresholds: 95% for phase 0 violations
- Multi-threaded inference (configurable thread count)

#### **incident_builder.py** — Event Packaging
- Combine:
  - Inference results (detections, confidence)
  - Vehicle telemetry (speed, location, timestamp)
  - Camera metadata (frame ID, timestamp)
- Output: Incident JSON with:
  - node_id, violation_type, plate
  - location (lat/lon), timestamp
  - confidence, evidence_url (S3 pre-signed)

#### **uploader.py** — Evidence Management
- Compress H.264 clips (7x ratio target)
- Encrypt with AES-256
- Queue for upload
- Local buffer: 16GB ring buffer (7-day retention)
- Resume on connectivity loss

### Main Event Loop

```python
async def main():
    camera = CameraCapture()
    obd = OBDInterface()
    gps = GPSModule()
    modem = CellularModem()
    inference = EdgeInference()
    
    while True:
        frame = camera.get_frame()
        detections = inference.run(frame)
        
        if detections.confidence > threshold:
            speed = obd.read_speed()
            location = gps.get_fix()
            incident = IncidentBuilder.build(detections, speed, location)
            uploader.queue_incident(incident)
        
        await asyncio.sleep(0.033)  # ~30fps
```

## Configuration

### gpio_pinout.yaml
```yaml
camera_interface: "MIPI CSI-2"
obd_ii:
  uart: "UART0"
  pins: [8, 10]
  baudrate: 38400
gps:
  uart: "UART1"
  pins: [27, 28]
  baudrate: 115200
power_management:
  battery_low: 17
  buck_enable: 27
```

### inference_config.json
```json
{
  "models": {
    "alpr": "models/alpr.tflite",
    "lane_detection": "models/lane_detection.tflite",
    "object_detection": "models/object_detection.tflite"
  },
  "confidence_thresholds": {
    "bus_lane": 0.95,
    "red_light": 0.95
  },
  "inference_settings": {
    "num_threads": 2,
    "enable_gpu": false,
    "max_detections": 100
  }
}
```

### network_config.yaml
```yaml
cellular:
  modem: "Quectel EC25"
  apn: "carrier_apn"
  bands: ["B3", "B7", "B20"]
  fallback_2g: true
backend:
  url: "https://api.civicmesh.local"
  upload_endpoint: "/incidents/submit"
  heartbeat_interval: 300
local_buffer:
  max_size_gb: 16
  retention_days: 7
```

## Installation (Phase 1)

```bash
# Cross-compile for Raspberry Pi CM4
./build_firmware.sh arm

# Install on RPi CM4
scp firmware.zip pi@node.local:/tmp/
ssh pi@node.local
unzip /tmp/firmware.zip
cd firmware
python main.py
```

## Testing

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Coverage report
pytest --cov=firmware --cov-report=html
```

## Development Workflow

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Locally (Without Hardware)
```bash
# Mock mode (simulates sensors)
python main.py --mock
```

### Deploy to Node
```bash
./deploy.sh <node_ip>
```

## Performance Targets

- **Inference Latency:** <100ms per frame
- **Throughput:** 30 frames/second
- **Memory Usage:** <200MB
- **CPU Usage:** <60% (single core)
- **Uptime:** >99% (with 15-18hr battery backup)
- **Data Loss:** Zero (local buffer + retry logic)

## Documentation

- [Hardware BOM](https://github.com/TrafficMesh/civicmesh-hardware/blob/main/bom/NODE_BOM.md) - Component list
- [GPIO Pinout](https://github.com/TrafficMesh/civicmesh-hardware/blob/main/firmware-requirements/gpio-pinout.md) - Pin assignments
- [Network Config](config/network_config.yaml) - Cellular setup
- [Central Docs Hub](https://github.com/TrafficMesh/civicmesh-docs) - Architecture, compliance, roadmap

## Phase 0 vs Phase 1

**Phase 0 (Now):** Hardware nodes + backend ingestion  
**Phase 1 (Q3 2026):** Firmware implementation with TFLite edge inference

## Contributing

See [CONTRIBUTING.md](https://github.com/TrafficMesh/civicmesh-docs/blob/main/community/CONTRIBUTING.md) in the docs repository.

## Team

- **Owner:** @TrafficMesh/firmware-team
- **Hardware Tech Lead:** civicmesh-hardware team

## License

Dual license: AGPL (open source) + BSL (commercial)
