#!/usr/bin/env python3

import lgpio
import time
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read("/etc/fancontrol/fan.conf")

# Read settings from config file
MAX_TEMP = int(config["fan"].get("max_temp", 50))
FAN_PIN = int(config["fan"].get("fan_pin", 14))
COOL_DURATION = int(config["fan"].get("cool_duration", 5))
CHECK_INTERVAL = int(config["fan"].get("check_interval", 5))

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Claim GPIO pin as an output
lgpio.gpio_claim_output(h, FAN_PIN)

# Function to read CPU temperature
def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        return float(file.read()) / 1000  # Convert millidegrees to Celsius

try:
    while True:
        temp = get_cpu_temp()
        print(f"CPU Temperature: {temp:.1f}°C (Threshold: {MAX_TEMP}°C)")

        if temp >= MAX_TEMP:
            print("Temperature above threshold - Turning ON fan")
            lgpio.gpio_write(h, FAN_PIN, 1)  # Turn ON fan
            time.sleep(COOL_DURATION)
        else:
            print("Temperature below threshold - Turning OFF fan")
            lgpio.gpio_write(h, FAN_PIN, 0)  # Turn OFF fan

        time.sleep(CHECK_INTERVAL)  # Check temperature again after interval

except KeyboardInterrupt:
    print("\nStopping fan control...")
    lgpio.gpio_write(h, FAN_PIN, 0)  # Ensure fan is OFF before exiting
    lgpio.gpiochip_close(h)
