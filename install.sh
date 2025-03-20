#!/bin/bash

echo "Installing Fan Control Service..."

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Try again with sudo." 
   exit 1
fi

# Create required directories
mkdir -p /etc/fancontrol
mkdir -p /usr/lib/fancontrol

# Move configuration file
cp fancontrol/fan.ini /etc/fancontrol/fan.ini
chmod 644 /etc/fancontrol/fan.ini

# Move Python script
cp fancontrol/fan_control.py /usr/lib/fancontrol/fan_control.py
chmod +x /usr/lib/fancontrol/fan_control.py

# Move systemd service file
cp fancontrol/fancontrol.service /etc/systemd/system/fancontrol.service

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable fancontrol.service
systemctl start fancontrol.service

echo "Installation complete! Check the service with:"
echo "  sudo systemctl status fancontrol.service"
