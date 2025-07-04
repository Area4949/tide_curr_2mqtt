# tide_curr_2mqtt
Python script for publishing tide data created from xtide (https://flaterco.com/xtide/) to mqtt broker.
Two topics are published to the mqtt broker.
  1) water_elevation : The current computed water elevation
  2) rate: The current water elevation change rate

This python program is meant to be run via a crontab job, with the tide station as an input variable. eg: */5 * * * * /usr/bin/python3 /home/usr/tide_curr_2mqtt.py "Anchorage"

Prerequisites are:
  1) python3
  2) Install Xtide from https://flaterco.com/xtide/
  3) install paho.mqtt python module

Sample output:

 - xtide/Anchorage/rate:
   1.9790399999999408

 - xtide/Anchorage/water_elevation:
   22.700862

# tide_hilo_2mqtt
Python script for publishing tide data created from xtide (https://flaterco.com/xtide/) to mqtt broker.
One topic is published to the mqtt broker.
  1) next_event : The next high or low tide event

This python program is meant to be run via a crontab job, with the tide station as an input variable. eg: */6 * * * * /usr/bin/python3 /home/usr/tide_hilo_2mqtt.py "Anchorage"

Prerequisites are:
  1) python3
  2) Install Xtide from https://flaterco.com/xtide/
  3) install paho.mqtt python module

Sample output:
  - xtide/Anchorage/next_event:
  {
  "date": "2025-06-05",
  "time": "4:31 PM AKDT",
  "elevation": "23.77",
  "event_type": "High Tide"
}
