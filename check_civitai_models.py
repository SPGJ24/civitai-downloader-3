import requests
import os
import json

CIVITAI_CREATOR_ID = "YOUR_CREATOR_ID"  # Replace with the creator's ID
CIVITAI_TOKEN = os.getenv("CIVITAI_TOKEN")  # Use GitHub secret
API_URL = f"https://civitai.com/api/v1/models?creatorId={CIVITAI_CREATOR_ID}"

# Load previously stored model data
LAST_MODEL_FILE = "last_model.json"
if os.path.exists(LAST_MODEL_FILE):
    with open(LAST_MODEL_FILE, "r") as f:
        last_model = json.load(f)
else:
    last_model = {}

# Fetch latest models from CivitAI
headers = {"Authorization": f"Bearer {CIVITAI_TOKEN}"}
response = requests.get(API_URL, headers=headers)
models = response.json().get("items", [])

if models:
    latest_model = models[0]
    model_id = latest_model["id"]
    version_id = latest_model["modelVersions"][0]["id"] if "modelVersions" in latest_model else ""
    file_format = "safetensors"  # Default, can be adjusted
    
    # Check if it's a new model
    if last_model.get("id") != model_id:
        with open("latest_model_id.txt", "w") as f:
            f.write(str(model_id))
        with open("latest_version_id.txt", "w") as f:
            f.write(str(version_id))
        with open("latest_file_format.txt", "w") as f:
            f.write(file_format)
        with open(LAST_MODEL_FILE, "w") as f:
            json.dump({"id": model_id, "version_id": version_id}, f)
        print("::set-env name=NEW_MODEL_FOUND::true")
    else:
        print("No new models found.")
else:
    print("No models available.")
