#!/usr/bin/env python3
import subprocess
import re
import time
import sys
import json
from paho.mqtt import client as mqtt_client
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"  # Replace with your MQTT broker address
MQTT_PORT = 1883
MQTT_USERNAME = "emqx"          # Replace with your MQTT username
MQTT_PASSWORD = "mypassword"    # Replace with your MQTT password


def get_first_tide_event(LOCATION):
    """Get next tide event from XTide"""
    try:
        output = subprocess.check_output(
            ["tide", "-l", LOCATION],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

# Regular expression to match either "High Tide" or "Low Tide"
        pattern = r".*?(High Tide|Low Tide)"
        match = match = re.search(pattern, output)
        if match:
            print("First occurrence:", match.group(0))
        else:
            print("No match found.")

        if match:
            line = match.group(0)
            parts = line.strip().split()
            date_str = parts[0]
            time_str = parts[1] + ' ' + parts[2] + ' ' + parts[3]  # Time and timezone
            elevation = parts[4]
            event_type = ' '.join(parts[6:])
                
            return {
                'date': date_str,
                'time': time_str,
                'elevation': elevation,
                'event_type': event_type,
            }

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"XTide error: {e}")
    return None


def mqtt_connect(client_id):
    """Connect to MQTT broker"""
    client = mqtt_client.Client(client_id)
    
    # For authenticated brokers:
    # Set username and password for authentication# client.username_pw_set('username', 'password')
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <location>")
        sys.exit(1)
    
    LOCATION = sys.argv[1]
    client = mqtt_connect(f'xtide-publisher-{LOCATION}')
    
#    while True:
    tide_event = get_first_tide_event(LOCATION)
    if tide_event:
        payload = json.dumps(tide_event)
        MQTT_TOPIC = "xtide/" + LOCATION + "/next_event"
        result = client.publish(MQTT_TOPIC, payload, qos=1, retain=True)
        status = "SUCCESS" if result.rc == mqtt_client.MQTT_ERR_SUCCESS else "FAILED"
        
#        time.sleep(300)  # Update every 5 minutes

if __name__ == "__main__":
    main()

