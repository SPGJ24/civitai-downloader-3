import requests
import os
import json

CIVITAI_CREATOR_ID = "RUN165"  # Replace with the creator's ID
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

# Debug: Print API response
print("API Response:", response.json())

models = response.json().get("items", [])

if models:
    latest_model = models[0]
    model_id = latest_model["id"]
    version_id = latest_model["modelVersions"][0]["id"] if "modelVersions" in latest_model else ""
    file_format = "safetensors"  # Default, can be adjusted
    
    # Debug: Print latest model details
    print("Latest Model ID:", model_id)
    print("Latest Version ID:", version_id)
    print("Last Model ID:", last_model.get("id"))
    
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
        
        # Set environment variable using environment file
        with open(os.environ["GITHUB_ENV"], "a") as f:
            f.write("NEW_MODEL_FOUND=true\n")
        
        # Print the download URL for debugging
        if version_id:
            download_url = f"https://civitai.com/api/download/models/{version_id}?type=Model&format={file_format}&token={CIVITAI_TOKEN}"
        else:
            download_url = f"https://civitai.com/api/download/models/{model_id}?type=Model&format={file_format}&token={CIVITAI_TOKEN}"
        print(f"Download URL: {download_url}")
        
        print("New model found. Environment variable set.")
    else:
        print("No new models found.")
else:
    print("No models available.")
