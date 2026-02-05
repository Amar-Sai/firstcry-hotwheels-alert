import json
import os

def load_states(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_states(path, states):
    with open(path, "w") as f:
        json.dump(states, f, indent=2)
