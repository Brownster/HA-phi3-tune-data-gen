import json
import random
import uuid

# Custom entities based on your Home Assistant setup
entities = {
    "sensor": ["carbon_dioxide", "carbon_monoxide", "outside_humidity", "outside_temperature", "movement_backyard"],
    "fan": ["ceiling_fan", "living_room_fan"],
    "light": ["ceiling_lights", "kitchen_lights"],
    "switch": ["decorative_lights"],
    "humidifier": ["dehumidifier", "humidifier", "hygrostat"],
    "water_heater": ["demo_water_heater"],
    "climate": ["ecobee", "heatpump", "hvac"],
    "cover": ["garage_door", "hall_window", "kitchen_window", "living_room_window"],
    "media_player": ["group", "kitchen", "living_room", "lounge_room"],
    "todo": ["shopping_list"]
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
    ],
    "add_to_list": [
        "Add {} to the {}",
        "Put {} on the {}",
        "Include {} in the {}"
    ]
}

def generate_synthetic_data(num_examples=100):
    synthetic_data = []
    
    for _ in range(num_examples):
        intent = random.choice(list(intents.keys()))
        entity_type = random.choice(list(entities.keys()))
        entity = random.choice(entities[entity_type])
        
        user_command_template = random.choice(intents[intent])
        if intent == "set_temperature":
            temperature = random.randint(60, 80)
            user_command = user_command_template.format(entity, temperature)
            tool_call = {
                "tool_name": "set_temperature",
                "tool_args": {
                    "entity_id": f"{entity_type}.{entity}",
                    "temperature": temperature
                },
                "platform": "homeassistant",
                "context": {
                    "user_prompt": user_command,
                    "language": "en"
                }
            }
            ha_response = f"The {entity} temperature has been set to {temperature} degrees."
        elif intent == "set_mode":
            mode = random.choice(["cool", "heat", "fan_only", "auto"])
            user_command = user_command_template.format(entity, mode)
            tool_call = {
                "tool_name": "set_mode",
                "tool_args": {
                    "entity_id": f"{entity_type}.{entity}",
                    "mode": mode
                },
                "platform": "homeassistant",
                "context": {
                    "user_prompt": user_command,
                    "language": "en"
                }
            }
            ha_response = f"The {entity} mode has been set to {mode}."
        elif intent in ["dim", "increase_brightness"]:
            brightness = random.randint(1, 100)
            user_command = user_command_template.format(entity)
            tool_call = {
                "tool_name": "turn_on",
                "tool_args": {
                    "entity_id": f"{entity_type}.{entity}",
                    "brightness_pct": brightness
                },
                "platform": "homeassistant",
                "context": {
                    "user_prompt": user_command,
                    "language": "en"
                }
            }
            ha_response = f"The brightness of {entity} has been set to {brightness}%."
        elif intent == "add_to_list":
            item = random.choice(["milk", "bread", "eggs", "cheese"])
            user_command = user_command_template.format(item, entity)
            tool_call = {
                "tool_name": "add_to_list",
                "tool_args": {
                    "item": item
                },
                "platform": "homeassistant",
                "context": {
                    "user_prompt": user_command,
                    "language": "en"
                }
            }
            ha_response = f"{item} has been added to your {entity.replace('_', ' ')}."
        else:
            user_command = user_command_template.format(entity)
            tool_call = {
                "tool_name": intent,
                "tool_args": {
                    "entity_id": f"{entity_type}.{entity}"
                },
                "platform": "homeassistant",
                "context": {
                    "user_prompt": user_command,
                    "language": "en"
                }
            }
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
        
        # Add system message with current states of entities
        current_states = {f"{entity_type}.{entity}": random.choice(["on", "off", "locked", "unlocked", "72 degrees", "idle"]) for entity_type in entities for entity in entities[entity_type]}
        system_message = {
            "role": "system",
            "content": f"You are a virtual assistant. The current state of devices is as follows: {', '.join([f'{k}: {v}' for k, v in current_states.items()])}. Use these states to respond accurately to user commands."
        }
        
        llm_reply = f"{ha_response} How else can I assist you?"
        
        data_point = {
            "id": str(uuid.uuid4()),
            "user_command": user_command,
            "parsed_intent": intent,
            "entity_information": f"{entity_type}.{entity}",
            "tool_call": tool_call,
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
