import json
import random
import requests

def convert_mmss_to_hhmmss(duration):
    if ':' not in duration:
        raise ValueError("Invalid duration format. Expected format: 'mm:ss' or 'hh:mm:ss'")

    parts = duration.split(':')
    if len(parts) == 2:
        # duration is in mm:ss format
        minutes, seconds = int(parts[0]), int(parts[1])
        if minutes < 60:
            # duration is less than 1 hour
            return f"{minutes:02d}:{seconds:02d}"
        else:
            # duration is 1 hour or more
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours:01d}:{minutes:02d}:{seconds:02d}"
    elif len(parts) == 3:
        # duration is already in hh:mm:ss format
        return duration
    else:
        raise ValueError("Invalid duration format. Expected format: 'mm:ss' or 'hh:mm:ss'")

def convert_seconds_to_hhmmss(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60

    if hours == 0:
        return f"{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:01d}:{minutes:02d}:{seconds:02d}"

try:
    response = requests.get('https://raw.githubusercontent.com/Sibu07/my_json/main/updated-calls.json')
    response.raise_for_status()
    json_data = json.loads(response.content)
except requests.exceptions.RequestException as e:
    print("Error: Unable to fetch data from the URL.")
    print(e)
    json_data = []

try:
    with open('data_hhmmss.json', 'r') as f:
        data_hhmmss = json.load(f)
except FileNotFoundError:
    data_hhmmss = []
except json.decoder.JSONDecodeError:
    print("Error: Invalid JSON format in the file.")
    data_hhmmss = []

try:
    with open('data_mmss.json', 'r') as f:
        data_mmss = json.load(f)
except FileNotFoundError:
    data_mmss = []
except json.decoder.JSONDecodeError:
    print("Error: Invalid JSON format in the file.")
    data_mmss = []

for item in json_data:
    call_duration = item['call_duration']
    time = item['time']

    try:
        if ':' in call_duration:
            # duration is in hh:mm:ss or mm:ss format
            call_duration = convert_mmss_to_hhmmss(call_duration)
        else:
            # duration is in seconds format
            call_duration = convert_seconds_to_hhmmss(int(call_duration))
    except ValueError as e:
        print(e)
        continue

    # Generate a random internet speed value between 0.1 to 9.1 with two decimal places
    internet_speed = round(random.uniform(0.1, 9.1), 1)

    mobile_charge = str(random.randint(10, 90))

    call_data = {
        "time": time,
        "Internet_speed": str(internet_speed),
        "call_duration": call_duration,
        "mobile_charge": mobile_charge.replace("\"", "\\\"")
    }

    if len(call_duration.split(':')) == 3:
        data_hhmmss.append(call_data)
    else:
        data_mmss.append(call_data)

with open('data_hhmmss.json', 'w') as f:
    json.dump(data_hhmmss, f)

with open('data_mmss.json', 'w') as f:
    json.dump(data_mmss, f)

print("Data saved successfully.")
