#!/usr/bin/env python3
import subprocess
import re
import time
import sys
from paho.mqtt import client as mqtt_client

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"  # Replace with your MQTT broker address
MQTT_PORT = 1883
MQTT_USERNAME = "emqx"          # Replace with your MQTT username
MQTT_PASSWORD = "mypassword"    # Replace with your MQTT password

def get_xtide_elevation(LOCATION):
    """Get current water elevation from XTide"""
    try:
        output = subprocess.check_output(
            ["tide", "-l", LOCATION, "-mm"],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        match = re.findall(r'(?<=\n)(.*?)(?=\n)', output)
        match = match[1]
        match = match.split()[-1]
        print (match)

        if match:
            return float(match)

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
    
    elevation = get_xtide_elevation(LOCATION)
    if elevation is not None:
        MQTT_TOPIC = "xtide/" + LOCATION + "/water_elevation"
        result = client.publish(MQTT_TOPIC, str(elevation), qos=1, retain=True)
        status = "SUCCESS" if result.rc == mqtt_client.MQTT_ERR_SUCCESS else "FAILED"
        print(f"Published {elevation}ft - {status}")
        print(elevation)
    time.sleep(15)
    elevation2 = get_xtide_elevation(LOCATION)
    if ((elevation is not None) and (elevation2 is not None)):
        rate = ((elevation2 - elevation) * 3600/15) 
        MQTT_TOPIC = "xtide/" + LOCATION + "/rate"
        result = client.publish(MQTT_TOPIC, str(rate), qos=1, retain=True)
        status = "SUCCESS" if result.rc == mqtt_client.MQTT_ERR_SUCCESS else "FAILED"
        
if __name__ == "__main__":
    main()
