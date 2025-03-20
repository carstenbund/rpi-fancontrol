# Fan Control System

This repository contains the systemd service and configuration for automatic fan control based on CPU temperature.

## **1. Configuration File**
Path: `/etc/fancontrol/fan.ini`

```ini
[fan]
max_temp = 50  # Temperature threshold in Celsius
fan_pin = 14  # GPIO pin for the fan
cool_duration = 5  # How long the fan stays on (seconds)
check_interval = 5  # How often to check the temperature (seconds)
```

## **2. Fan Control Script**
Path: `/usr/lib/fancontrol/fan_control.py`

This script:
- Reads CPU temperature
- Turns fan **ON** if temperature >= `max_temp`
- Turns fan **OFF** when cooler
- Reads settings from `/etc/fancontrol/fan.ini`

## **3. Systemd Service File**
Path: `/etc/systemd/system/fancontrol.service`

```ini
[Unit]
Description=Fan Control Service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /usr/lib/fancontrol/fan_control.py
Restart=always
User=root
WorkingDirectory=/usr/lib/fancontrol/
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## **4. Installation Instructions**
```bash
sudo mkdir -p /etc/fancontrol
sudo mkdir -p /usr/lib/fancontrol

sudo mv fan_control.py /usr/lib/fancontrol/
sudo chmod +x /usr/lib/fancontrol/fan_control.py

sudo mv fancontrol.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fancontrol
sudo systemctl start fancontrol
```

Check status:
```bash
sudo systemctl status fancontrol
```
