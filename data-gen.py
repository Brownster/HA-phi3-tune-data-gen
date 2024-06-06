import json
import random
import uuid

# Expanded data for synthetic generation with more intent variations
entities = {
    "light": ["living_room_light", "kitchen_light", "bedroom_light"],
    "thermostat": ["main_thermostat", "bedroom_thermostat"],
    "sensor": ["basement_humidity", "kitchen_temperature", "outdoor_motion"],
    "lock": ["front_door", "back_door", "garage_door"],
    "vacuum": ["robot_vacuum"],
    "camera": ["front_door_camera", "backyard_camera"],
    "alarm": ["home_alarm", "garage_alarm"],
    "blind": ["living_room_blinds", "bedroom_blinds"],
    "fan": ["ceiling_fan", "desk_fan"],
    "switch": ["garden_lights_switch", "living_room_switch"]
}

intents = {
    "turn_on": [
        "Turn on the {}", 
        "Activate the {}",
        "Switch on the {}",
        "Power up the {}"
    ],
    "turn_off": [
        "Turn off the {}", 
        "Deactivate the {}",
        "Switch off the {}",
        "Power down the {}"
    ],
    "set_temperature": [
        "Set the {} to {} degrees", 
        "Adjust the {} to {} degrees",
        "Change the {} temperature to {} degrees"
    ],
    "get_status": [
        "What's the status of the {}",
        "Check the {} status",
        "How is the {} doing",
        "Give me the status of the {}"
    ],
    "lock": [
        "Lock the {}", 
        "Secure the {}",
        "Engage the {} lock"
    ],
    "unlock": [
        "Unlock the {}", 
        "Unsecure the {}",
        "Disengage the {} lock"
    ],
    "start": [
        "Start the {}", 
        "Begin the {}",
        "Initiate the {}"
    ],
    "stop": [
        "Stop the {}", 
        "Halt the {}",
        "Terminate the {}"
    ],
    "enable": [
        "Enable the {}", 
        "Activate the {}",
        "Turn on the {}"
    ],
    "disable": [
        "Disable the {}", 
        "Deactivate the {}",
        "Turn off the {}"
    ],
    "open": [
        "Open the {}", 
        "Raise the {}",
        "Lift the {}"
    ],
    "close": [
        "Close the {}", 
        "Lower the {}",
        "Shut the {}"
    ],
    "dim": [
        "Dim the {}", 
        "Reduce the brightness of the {}",
        "Lower the brightness of the {}"
    ],
    "increase_brightness": [
        "Increase the brightness of the {}",
        "Brighten the {}",
        "Raise the brightness of the {}"
    ],
    "set_mode": [
        "Set the {} to {} mode", 
        "Change the {} to {} mode",
        "Switch the {} to {} mode"
    ]
}

api_endpoints = {
    "turn_on": "/api/services/{}/turn_on",
    "turn_off": "/api/services/{}/turn_off",
    "set_temperature": "/api/services/thermostat/set_temperature",
    "get_status": "/api/states/{}",
    "lock": "/api/services/lock/lock",
    "unlock": "/api/services/lock/unlock",
    "start": "/api/services/{}/start",
    "stop": "/api/services/{}/stop",
    "enable": "/api/services/alarm_control_panel/alarm_arm_away",
    "disable": "/api/services/alarm_control_panel/alarm_disarm",
    "open": "/api/services/cover/open_cover",
    "close": "/api/services/cover/close_cover",
    "dim": "/api/services/light/turn_on",  # Assuming dimming is part of turning on the light with brightness
    "increase_brightness": "/api/services/light/turn_on",
    "set_mode": "/api/services/{}/set_mode"
}

def generate_synthetic_data(num_examples=100):
    synthetic_data = []
    
    for _ in range(num_examples):
        intent = random.choice(list(intents.keys()))
        valid_entities = [entity for entity in entities if entity in api_endpoints[intent]]
        entity_type = random.choice(valid_entities)
        entity = random.choice(entities[entity_type])
        
        user_command_template = random.choice(intents[intent])
        if intent == "set_temperature":
            temperature = random.randint(60, 80)
            user_command = user_command_template.format(entity, temperature)
            api_payload = json.dumps({"entity_id": entity, "temperature": temperature})
            ha_response = f"The {entity} temperature has been set to {temperature} degrees."
        elif intent == "set_mode":
            mode = random.choice(["cool", "heat", "fan_only", "auto"])
            user_command = user_command_template.format(entity, mode)
            api_payload = json.dumps({"entity_id": entity, "mode": mode})
            ha_response = f"The {entity} mode has been set to {mode}."
        elif intent in ["dim", "increase_brightness"]:
            brightness = random.randint(1, 100)
            user_command = user_command_template.format(entity)
            api_payload = json.dumps({"entity_id": entity, "brightness_pct": brightness})
            ha_response = f"The brightness of {entity} has been set to {brightness}%."
        else:
            user_command = user_command_template.format(entity)
            api_payload = json.dumps({"entity_id": entity})
            if intent.startswith("turn"):
                ha_response = f"The {entity} has been turned {'on' if 'on' in intent else 'off'}."
            elif intent == "lock":
                ha_response = f"The {entity} has been locked."
            elif intent == "unlock":
                ha_response = f"The {entity} has been unlocked."
            elif intent == "start":
                ha_response = f"The {entity} has been started."
            elif intent == "stop":
                ha_response = f"The {entity} has been stopped."
            elif intent == "enable":
                ha_response = f"The {entity} has been enabled."
            elif intent == "disable":
                ha_response = f"The {entity} has been disabled."
            elif intent == "open":
                ha_response = f"The {entity} has been opened."
            elif intent == "close":
                ha_response = f"The {entity} has been closed."
            elif intent == "get_status":
                ha_response = f"The status of {entity} is {'on' if 'on' in intent else 'off'}."
        
        api_endpoint = api_endpoints[intent].format(entity_type)
        api_response = {"result": "success", "status_code": 200}
        
        # Add system message with current states of entities
        current_states = {entity: random.choice(["on", "off", "locked", "unlocked", "72 degrees", "idle"]) for entity_list in entities.values() for entity in entity_list}
        system_message = {
            "role": "system",
            "content": f"You are a virtual assistant. The current state of devices is as follows: {', '.join([f'{k}: {v}' for k, v in current_states.items()])}. Use these states to respond accurately to user commands."
        }
        
        llm_reply = f"{ha_response} How else can I assist you?"
        
        data_point = {
            "id": str(uuid.uuid4()),
            "user_command": user_command,
            "parsed_intent": intent,
            "entity_information": entity,
            "api_request": {
                "endpoint": api_endpoint,
                "payload": api_payload,
                "headers": {"Authorization": "Bearer TOKEN", "Content-Type": "application/json"}
            },
            "api_response": api_response,
            "contextual_information": current_states,
            "system_message": system_message,
            "ha_response": ha_response,
            "llm_reply": llm_reply
        }
        
        synthetic_data.append(data_point)
    
    return synthetic_data

# Generate synthetic data
synthetic_dataset = generate_synthetic_data(100)

# Save to JSONL file
with open("synthetic_dataset.jsonl", "w") as f:
    for item in synthetic_dataset:
        f.write(json.dumps(item) + "\n")

print("Synthetic dataset generated and saved to synthetic_dataset.jsonl")
